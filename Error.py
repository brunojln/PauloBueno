import org.jblas.DoubleMatrix

class Error:
    @staticmethod
    def error(new_r, r):
        new_r_norm = abs(new_r.norm2())
        r_norm = abs(r.norm2())
        error = abs(new_r_norm - r_norm)
        return error