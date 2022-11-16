from scipy.spatial import distance
from constants import ML_PRED
from sklearn.preprocessing import StandardScaler

class RecommendSongs:
    """A collaboraitve system to recommend similar songs based on a variety of numerical metrics extracted. 

    Future versions to include:
    * categorical variable support
    * user similarity matrix
    * seasonality to adjust with drastic data drift (holiday changeover)"""

    def __init__(self, music_data, song, n_predictions=10):
        self.model_data = music_data
        self.test_song = song

        self.preprocessed_model_data = self._preprocess()
        self.model_data[ML_PRED] = self.preprocessed_model_data.apply(lambda x: self._distance(x), axis=1)
        self.predictions = self.model_data.sort_values(by=[ML_PRED]).head(n_predictions)

    def _preprocess(self):
        return StandardScaler().fit_transform(self.model_data)

    def _distance(self, input_vector):
        return distance.cosine(list(self.test_song.values), input_vector)
