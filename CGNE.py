import org.jblas.DoubleMatrix

class CGNE:
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
            alpha = r.transpose().mmul(r) / p.transpose().mmul(p)
            new_f = f + alpha.mmul(p)
            new_r = r - alpha.mmul(h.mmul(p))
            beta = new_r.transpose().mmul(new_r) / r.transpose().mmul(r)
            new_p = h.transpose().mmul(new_r) + beta.mmul(p)

            error = self.error(new_r, r)

            f = new_f
            r = new_r
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