package Matriz;

import org.jblas.DoubleMatrix;

public class CGNR {
    
    public int iteractions = 0;
    public DoubleMatrix getImage(DoubleMatrix H, DoubleMatrix g, Integer selectedModelFlag) {
        System.out.println("H rows: " + H.rows + " x " + H.columns + " and g rows: " + g.columns);

        DoubleMatrix f = DoubleMatrix.zeros(H.columns);
        DoubleMatrix r = g.sub(H.mmul(f));

        DoubleMatrix z = H.transpose().mmul(r);
        DoubleMatrix p = z;
        int i = 0;

        do{
            DoubleMatrix w = H.mmul(p);
            Double z_squared = z.norm2() * z.norm2();
            Double w_squared = w.norm2() * w.norm2();

            Double alpha = z_squared / w_squared;
            
            DoubleMatrix f1 = f.add(p.mul(alpha));
            DoubleMatrix r1 = r.sub(w.mul(alpha));
            DoubleMatrix z1 = H.transpose().mmul(r1);

            Double z1_squared = z1.norm2() * z1.norm2();
            Double beta = z1_squared / z_squared;
            DoubleMatrix p1 = z1.add(p.mul(beta));

            f = f1;
            r = r1;
            z = z1;
            p = p1;
            i++;

        }while(i < 30);

        if (selectedModelFlag == 1) {
            f.reshape(60, 60);
        }
        else {
            f.reshape(30, 30);
        }

        return f;
    }
}
