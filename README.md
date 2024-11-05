# Head Motion Prediction Lab

## Development Environment Setup
### CPU Anaconda environment

1. Install the Anaconda environment and activate it:
```bash
conda env create -f tf-cpu-dev.yaml
conda activate tf-cpu-dev
```

3. Test the code
```bash
pytest
```

### CPU Docker Environment

1. Build the Docker image
```bash
sudo docker build -t mpl-cpu .
```

2. Start a container
```bash
docker run -it\
    -v /path/to/code:/opt/motion-prediction-lab\
    --network host\
    mpl-cpu
```

3. Now is a connection to a local Jupyter server possible. Run them on first run in order


### GPU Docker Environment with ROCm 

1. Build the Docker image
```bash
sudo docker build -t mpl-gpu - < rocm.Dockerfile
```

2. Run it in a container
```bash
sudo docker run -it\
    --volume /path/to/code:/opt/motion-prediction-lab\
    --network host\
    --device=/dev/kfd\
    --device=/dev/dri\
    --security-opt seccomp=unconfined\
    --group-add video\
    mpl-rocm
```

3. Now is a connection to a local Jupyter server possible. Run them on first run in order.
**WARNING**: TensorFlow reservers a great part of your GPUs memory by default, so notebooks using it shouldnt be used in parallel. Otherwise the machine may run unstable. (Reset kernel after done)


## Usage

1. Start a Jupyter server in the `notebooks` directory or **skip this step if using docker**
2. Navigate to the Jupyter page in your browser (typically localhost:8888)
3. Run the notebooks in order
4. Optional: Start TensorBoard server (Does not work with docker yet)
```bash
tensorboard --logdir data/logs/fit
```