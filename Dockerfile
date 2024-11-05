FROM ubuntu:20.04

# Install pip and git
RUN apt-get update
RUN apt-get install -y python3-pip git

# Install python dependencies
RUN pip3 install tensorflow-rocm matplotlib pandas scikit-learn pytest jupyter statsmodels
RUN pip3 -q install pip --upgrade

RUN mkdir /opt/motion-prediction-lab
COPY . /opt/motion-prediction-lab

WORKDIR /opt/motion-prediction-lab/notebooks
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]