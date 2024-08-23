import numpy as np

class signalGain:
    @staticmethod
    def model(g, model):
        s = g.length // 64
        n = 64

        g = g.reshape(s, n)

        for c in range(g.columns):
            for l in range(g.rows):
                index = s * c + l
                gamma = 100 + 0.05 * l * np.sqrt(l)
                g[l, c] *= gamma

        return g.reshape(g.length, 1)

    # This commented-out method is not implemented in the Python version
    # as it requires additional details that were not provided.
    # @staticmethod
    # def gain_signal(model, g_path):
    #     if model == 1:  # Model 1
    #         n = 64
    #         s = 794
    #         size = 60
    #     else:  # Model 2
    #         n = 64
    #         s = 436
    #         size = 30
    #
    #     # r = CsvParser.read_float_matrix_from_csv_file(g_path, ',')
    #
    #     for c in range(n):
    #         for l in range(s):
    #             index = s * c + l
    #             signal = 100 + 1/20 * l * np.sqrt(l)
    #             r[index] *= signal
    #
    #     return r.toarray()