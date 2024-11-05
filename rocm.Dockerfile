FROM ubuntu:20.04

# Configure timezone, else it stops at installing tzdata
ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add the ROCm repository
RUN apt-get update && apt-get install -y wget gnupg2
RUN wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | apt-key add -
RUN echo 'deb [arch=amd64] https://repo.radeon.com/rocm/apt/debian/ xenial main' | tee /etc/apt/sources.list.d/rocm.list
RUN apt-get update

# Install ROCm and dependencies
RUN apt-get install -y libnuma-dev rocm-dev
RUN apt-get install -y rccl hipblas miopen-hip rocfft rocrand

# Install pip and git
RUN apt-get update
RUN apt-get install -y python3-pip git

# Install python dependencies
RUN pip3 install tensorflow-rocm matplotlib pandas scikit-learn pytest jupyter statsmodels

RUN mkdir /opt/motion-prediction-lab
COPY . /opt/motion-prediction-lab

WORKDIR /opt/motion-prediction-lab/notebooks
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]