import logging
from models.simple_ann import SimpleANN
from models.baseline import Baseline
from datatools import preprocessing as prep
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configure logger
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt='%Y-%m-%d-%H:%M:%S'
)

# Each entry defines a dataset to load and has the following parameters:
# type: One of 'train', 'validation' or 'test'
# path: The file path where the datasets resides
# values: The loaded table from the file as numpy array
#
# Multiple entries per type are possible
dataset=[
    {
        'type': "train",
        'path': "",
        'values': None
    },
    {
        'type': "validation",
        'path': "",
        'values': None
    },
    {
        'type': "test",
        'path': "",
        'values': None
    }
]

logging.info("Loading dataset from disk")
delimiter = ","
decimal = "."
header = 0  # First row is the header
for i in range(len(dataset)):
    logging.debug("Loading {}".format(dataset[i]['path']))
    df=pd.read_csv(dataset[i]['path'], delimiter=delimiter, decimal=decimal, header=header) 
    dataset[i]['values'] = df.to_numpy() # Use internally only numpy arrays

logging.info("Normalizing dataset")
# Derive normalization parameters only from training set,
data=np.vstack([d['values'] for d in dataset if d['type'] == 'train'])

# but apply to the whole set
target=np.vstack([d['values'] for d in dataset])

normalized=target # Remove this line and uncomment desired normalization function
#normalized=prep.normalize_mean_std(data, target)
#normalized=prep.normalize_standard_sca(data, target)
#normalized=prep.normalize_minmax_sca(data, target)
#normalized=prep.normalize_robust_sca(data, target)

# After normalization split the table proportional by the dataset lengths and save them
# Assumption: The ordering did not change between dataset array and table
start=0
for i in range(len(dataset)):
    end=start+len(dataset[i]['values'])
    dataset[i]['values']=normalized[start:end,:]
    start=end
    
# Now all normalized datasets can be read one by one and get windowed independently
logging.info("Windowing dataset")
X_train = []
y_train = []
X_validation = []
y_validation = []
X_test = []
y_test = []
for entry in dataset:
    X_part, y_part = prep.window_time_series(entry['values'][:, 1:8], windowsize=32, lat=1)

    if entry['type'] is 'train':
        X_train.append(X_part)
        y_train.append(y_part)
    if entry['type'] is 'validation':
        X_validation.append(X_part)
        y_validation.append(y_part)
    if entry['type'] is 'test':
        X_test.append(X_part)
        y_test.append(y_part)

X_train=np.vstack(X_train)
y_train=np.vstack(y_train)
X_validation=np.vstack(X_validation)
y_validation=np.vstack(y_validation)
X_test=np.vstack(X_test)
y_test=np.vstack(y_test)

model = SimpleANN()
logging.info('Training model')
# Train the model with the data
model.train(X_train, y_train, X_val=X_validation, y_val=y_validation)

logging.info('Testing model')
# Predict values with the trained model
y_pred = model.predict(X_validation)

# Generate baseline values
baseline = Baseline()
y_base = baseline.predict(X_validation)

t = np.arange(len(X_validation)) * 5  # 5ms is the sample time
plt.plot(t, y_validation[:, :, 0], label='Real')
plt.plot(t, y_base[:, :, 0], label='Baseline')
plt.plot(t, y_pred[:, :, 0], label='Prediction')
plt.legend(loc='upper left')  # Place legend in upper left corner
plt.xlabel('Time/ms')
plt.ylabel('x-Coordinate/m')
plt.show()
