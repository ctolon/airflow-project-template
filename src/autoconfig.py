import yaml
from typing import Union, Optional
import argparse


def load_yaml_config(config_path: str, load_keys: Optional[Union[list, str]] = None, flatten: bool = True) -> dict:
    """
    Load YAML configuration from a file and return a flattened dictionary.

    Args:
        config_path (str): Path to the YAML configuration file.
        load_keys (Optional[Union[list, str]], optional): A list of dictionary keys to extract from the YAML file,
            or a single string representing a dictionary key. Defaults to None.
        flatten (bool): If True load YAML config as flatten. Defaults to True.

    Returns:
        dict: A flattened or non-flattened dictionary of the YAML configuration.
    """

    # Define the constructors
    def construct_yaml_int(loader, node):
        return int(loader.construct_scalar(node))

    def construct_yaml_float(loader, node):
        return float(loader.construct_scalar(node))

    def construct_yaml_bool(loader, node):
        return loader.construct_scalar(node) == 'true'

    def construct_yaml_map(loader, node):
        loader.flatten_mapping(node)
        return dict(loader.construct_pairs(node))

    def flatten_dict(d):
        flat_dict = {}
        for k, v in d.items():
            flat_dict[k.replace('-', '_')] = v
        return flat_dict

    # Add the constructors to the SafeLoader
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:int', construct_yaml_int)
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:float', construct_yaml_float)
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:bool', construct_yaml_bool)
    yaml.SafeLoader.add_constructor('tag:yaml.org,2002:map', construct_yaml_map)

    print("Config YAML File Loading...")
    # Load Configs from yaml
    with open(config_path, "r") as f:
        if load_keys is None:
            config = yaml.safe_load(f)
        elif isinstance(load_keys, str):
            config = yaml.safe_load(f)[load_keys]
        else:
            config = yaml.safe_load(f)
            for key in load_keys:
                config = config[key]

    if flatten:
        return flatten_dict(config)
    else:
        return config


def jinja_handler(args: argparse.Namespace, yyyymmdd: str):
    args_as_dict = vars(args)
    for arg, parameter in args_as_dict.items():
        if isinstance(arg, str) and "strftime" in parameter:
            print(f"Jinja Epoch Handler Will applied for --> {arg}: {parameter}")
            args.arg = args.arg.replace("{{ now().strftime('%Y%m%d') }}", yyyymmdd)
            print(f"Jinja Output --> {arg} {parameter}")
    return args


def extract_args_from_yaml(config_path: str, load_keys: Optional[Union[list, str]] = None, load_as_dict: bool = False):
    config = load_yaml_config(config_path, load_keys)
    print("Config YAML File Loaded Successfully.")
    args = argparse.Namespace()
    args.__dict__.update(config)
    # args = jinja_handler(args)
    # print("Jinja Handler Process Finished Sucessfully.")
    if load_as_dict is True:
        return vars(args)
    return args


def extract_args_from_dict_as_namespace(input_dict: str,
                                        load_keys: Optional[Union[list, str]] = None) -> argparse.Namespace:
    """This function will convert a dictionary to argparse.Namespace.

    Args:
        input_dict (str): Input dictionary from Airflow Params.
        load_keys (Optional[Union[list, str]], optional): Which Keys should be loaded from dict. Defaults to None.

    Returns:
        argparse.Namespace: A Namespace object which includes Airflow Params.
    """

    if load_keys is not None:
        input_dict = input_dict[load_keys]
    elif isinstance(load_keys, str):
        input_dict = input_dict[load_keys]
    else:
        for key in load_keys:
            input_dict = input_dict[key]

    args = argparse.Namespace()
    args.__dict__.update(input_dict)
    return args


'''
# TODO Implement it
def fail_callback(context):
    """
    This function will be called whenever a task in the current DAG fails.
    It triggers a new DAG run with a DockerOperator if any task fails.
    """
    dag_id = 'call_on_failure'
    task_id = 'remove_files'
    execution_date = context['execution_date']

    # Trigger a new DAG run with the TriggerDagRunOperator
    trigger_op = TriggerDagRunOperator(
        task_id=f'trigger_for_remove_{dag_id}',
        trigger_dag_id=dag_id,
        execution_date=execution_date,
        conf={'task_to_trigger': task_id},
        dag=context['dag']
    )

    return trigger_op.execute(context=context)
'''
