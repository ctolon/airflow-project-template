from airflow.providers.docker.operators.docker import DockerOperator


class XComDockerOperator(DockerOperator):
    """Wrapper Docker Operator for send data using Xcom"""

    def post_execute(self, context, result=None):
        if self.cli is not None:
            self.log.info('Removing Docker container')
            self.cli.remove_container(self.container['Id'])
        super().post_execute(context, result)
