import numpy as np
import h5py

with h5py.File("test.h5", "w") as f:
    f.create_dataset(
        name="test",
        data=np.random.rand(5,5,5),
        shape=(5,5,5),
        compression="gzip",
        compression_opts=9,
    )