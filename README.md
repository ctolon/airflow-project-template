### Git Submodule Commands


```bash
# ==== Yeni submodule ekleme ====
git submodule add <url> <name>
```

```bash
# === sub modulleri recursive init etme ===
git submodule update --init --recursive
```
```bash
# === Git head'ini resetleme (Çok acil değilse kullanmayın) ===
git reset --hard HEAD
```

```bash
# === git submodullerinin statusunu göstermek ===
git submodule status
```

```bash
# === tüm sub modülleri güncelleme (git pull for every sub modules) ===
git submodule foreach git pull origin master
```

```bash
=== tüm sub modülleri init edip tek tek güncelleme ===
# Get the submodule initial
git submodule add ssh://bla submodule_dir
git submodule init
```

## Spesifik Branch'i sub module'e bağlama

Template:

```bash
git submodule set-branch -b <branch|tag> <path-to-submodule>
```

Örnek:

```bash
git submodule set-branch -b 0.2.25 projects/mlflow
```

# Docker Task Template

```python
    @task.docker(
        image=CommonDockerService.MLFLOW_IMG,
        container_name=_load_container(CommonDockerService.MLFLOW_SVC),
        api_version=DOCKER_API_VERSION,
        docker_url=DockerUrl.PROXY,
        network_mode=DockerNetwork.HOST,
        mounts=DockerServiceMounts.COMMON_STAGE,
        mount_tmp_dir=False,
        cpus=DockerCPU.FOUR,
        device_requests=DockerGPU.NONE,
        mem_limit=DockerMemory.EIGHT,
        auto_remove=True,
        user=0,
        multiple_outputs=True,
        working_dir=DockerDataProcessDirs.COMMON.as_posix(),
        environment={
            'PYTHONPATH': ScriptDirs.COMMON_SCRIPTS.as_posix(),
            'LIBS_TO_INJECT': CommonDockerService.MLFLOW
        }
    )
```
