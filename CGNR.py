import org.jblas.DoubleMatrix

class CGNR:
    def __init__(self):
        self.iterations = 0

    def get_image(self, h, g, selected_model_flag):
        f = DoubleMatrix.zeros(h.columns)
        r = g - h.mmul(f)
        z = h.transpose().mmul(r)
        p = z

        error = float('inf')
        i = 0
        while error > 1e-4 and i < 30:
            w = h.mmul(p)
            z_squared = z.norm2() ** 2
            w_squared = w.norm2() ** 2
            alpha = z_squared / w_squared

            new_f = f + p * alpha
            new_r = r - w * alpha
            new_z = h.transpose().mmul(new_r)
            new_z_squared = new_z.norm2() ** 2
            beta = new_z_squared / z_squared
            new_p = new_z + p * beta

            error = self.error(new_r, r)

            f = new_f
            r = new_r
            z = new_z
            p = new_p
            i += 1

        self.iterations = i

        if selected_model_flag == 1:
            f.reshape(60, 60)
        else:
            f.reshape(30, 30)

        return f

    def get_iterations(self):
        return self.iterations

    def error(self, new_r, r):
        return (new_r - r).norm2()