import numpy as np
import random



class EEG_SSL_Dataset(Dataset):

	def __init__(self, data_folder, T_pos_TS, T_neg_TS,\
	 			sampling_freq=100, window_length=30, predict_delay=60, batch_size=128):

		self.data_folder = data_folder
		self.T_pos_TS = int(T_pos_TS)
		self.T_neg_TS = int(T_neg_TS)
		self.batch_size = batch_size
		self.window_length = window_length
		self.predict_delay = predict_delay
		self.sampling_freq = sampling_freq
		self.files = [f for f in os.listdir(data_folder) if f.endswith("PSG.edf")]

		full_path = os.path.join(self.data_folder, self.files[0])
		preprocessed = preprocess(full_path)
        TS_dataset, TS_labels = temporal_shuffling(preprocessed, int(self.T_pos_TS), int(self.T_neg_TS), int(selfnum_samples))

		self.len = len(self.files) * preprocessed

	def __len__(self):


	def __getitem__(self, idx):
		"""

		"""

	def get_batch():
		minibatch_TS = []
		files = random.sample(self.files, int(num_users))
		for f in files:
			full_path = os.path.join(data_folder, f)
			preprocessed = preprocess(full_path)
			TS_dataset, TS_labels = temporal_shuffling(preprocessed, int(self.T_pos_TS), int(self.T_neg_TS), int(selfnum_samples))
			minibatch_TS.append((TS_dataset, TS_labels))

		return minibatch_TS

    def temporal_shuffling(epochs, T_pos, T_neg, num_samples):
        """ Builds a self-supervised (temporal shuffling) dataset of epochs

        Args:
            epochs - Numpy datset of time-series arrays
            T_pos - positive context to sample from
            T_neg - negative context to sample from
            num_samples - int representing number of epochs to sample

        Output:
            TS_dataset - Temporal Shuffling Dataset of dimensions (L, 4, s, c)
                L - # of samples = # of user * # of epochs per user * 6
                3 - sample1 + sample2 + sample3
                s - # of eeg channels in each sample
                c - Samples per channel = 30s * 128Hz
            TS_labels - Temporal Shuffling labels of dimensions (L, 1)
                for each y = {1: if sample1 < sample2 < sample3 and -1: otherwise}
        """
        total_samples = epochs.shape[0] * 6
        TS_dataset = np.empty((total_samples, 3, epochs.shape[1], 3867)) ##TODO change shape of dataset according to num_samples
        TS_labels = np.empty((total_samples, 1)) ##TODO change shape of dataset according to num_samples
        counter = 0

        for idx, sample1 in enumerate(epochs):
            sample1 = epochs[idx]
            for _ in range(3): # T_pos loop
                sample2_index = np.random.randint(max(idx-T_pos, 0), min(idx+T_pos, epochs.shape[0]-1))
                while sample2_index == idx: # should not be the same
                    sample2_index = np.random.randint(max(idx-T_pos, 0), min(idx+T_pos, epochs.shape[0]-1))
                sample2 = epochs[sample2_index]

                if idx-T_neg <= 0: # T_neg if (corners)
                    sample3_index = np.random.randint(idx+T_neg, epochs.shape[0])
                elif idx+T_neg >= epochs.shape[0]: # take care of low == high
                    sample3_index = np.random.randint(0, idx-T_neg)
                else:
                    sample3_index_1 = np.random.randint(idx+T_neg, epochs.shape[0])
                    sample3_index_2 = np.random.randint(0, idx-T_neg)
                    sample3_index = list([sample3_index_1, sample3_index_2])[int(random.uniform(0,1))]
                sample3 = epochs[sample3_index]

                if idx < sample2_index and sample2_index < sample3_index:
                    y = 1
                else:
                    y = -1

                TS_sample = np.array([sample1, sample2, sample3])
                TS_dataset[counter] = TS_sample
                TS_labels[counter] = y
                counter += 1

            for _ in range(3): # T_neg loop
                sample2_index = np.random.randint(max(idx-T_pos, 0), min(idx+T_pos, epochs.shape[0]-1))
                while sample2_index == idx: # should not be the same
                    sample2_index = np.random.randint(max(idx-T_pos, 0), min(idx+T_pos, epochs.shape[0]-1))
                sample2 = epochs[sample2_index]

                sample3_index = np.random.randint(max(idx-T_pos, 0), min(idx+T_pos, epochs.shape[0]-1))
                while sample2_index == sample3_index or sample3_index == idx: # should not be the same
                    sample3_index = np.random.randint(max(idx-T_pos, 0), min(idx+T_pos, epochs.shape[0]-1))
                sample3 = epochs[sample3_index]

                if idx < sample2_index and sample2_index < sample3_index:
                    y = 1
                else:
                    y = -1

                TS_sample = np.array([sample1, sample2, sample3])
                TS_dataset[counter] = TS_sample
                TS_labels[counter] = y
                counter += 1

        return TS_dataset, TS_labels
