import numpy as np

N_TABLE = np.array([[2,3,5,6,7,11,17], [3,4,7,9,11,19,35],\
                    [3,5,9,13,17,34,72], [4,6,11,17,26,57,146],\
                    [4,7,16,24,37,97,293], [4,8,20,33, 54,163,588],\
                    [5,9,26,44,78,272,1177]])
                    
class RANSAC():
    def __init__(self, data, model_class, min_samples, residual_threshold, max_trials):
        self.data = data
        self.model = model_class()
        self.min_samples = min_samples
        self.residual_threshold = residual_threshold 
        assert type(data) == np.ndarray
        self.inliers = np.full(data.shape, fill_value=False)
        self.N = max_trials
        self.d = 5.99*self.variance
        assert len(data.shape[1]) >= 2
        self.T = 0.8*len(data.shape[1])
    
    def __call__(self):
        current_subset = np.full((self.min_samples, self.data.shape[1]), fill_value=None)
        for _ in range(self.N):
            self.model.estimate(current_subset)
            count=0
            for i in range(self.data):
                if abs(self.data[i]-self.model.eval(self.data[i]) <= self.residual_threshold) and \
                        self.model.residual(self.data[i]) < self.d: 
                    count += 1
                    current_subset.append(self.data[i], axis=0)
            if count >= self.T: self.model.estimate(current_subset)
            return (self.model, self.inliers)
        return (self.model, self.inliers)
