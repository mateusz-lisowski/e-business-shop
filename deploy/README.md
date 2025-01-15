# Deploying prestashop service

> ⚠️ **Warning:** After each `ssh` command you have to provide a password. You can find it in the instruction for the cluster.

## Clone only this branch to your cluster
```commandline
git clone --branch deploy --single-branch https://github.com/mateusz-lisowski/e-business-shop.git
```

## Login to cluster

### SSH to swarm bastion
```commandline
ssh rsww@172.20.83.101
```

### SSH to swarm management server
```commandline
ssh hdoop@student-swarm01.maas
```

## Create an SSH tunnel to the database management web GUI

```commandline
ssh -L 5242:student-swarm01.maas:9099 rsww@172.20.83.101
```

Then you can access web GUI at: `http://localhost:5242`

## Main project directory
```commandline
cd /opt/storage/actina15-20/block-storage/students/projects/students-swarm-services/BE_193151
```

## Run stack
```commandline
docker stack deploy -c docker-compose.yaml BE_193151 --with-registry-auth
```

## Create an SSH tunnel to the prestashop instance

```commandline
ssh -L 19339:student-swarm01.maas:19339 rsww@172.20.83.101
```
