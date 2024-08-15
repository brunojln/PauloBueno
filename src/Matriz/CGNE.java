package Matriz;
import org.jblas.DoubleMatrix;

public class CGNE {
    public int iteractions = 0;

    public DoubleMatrix getImage(DoubleMatrix H, DoubleMatrix g, Integer selectedModelFlag){
        System.out.println("H rows: " + H.rows + " x " + H.columns + " and g rows: " + g.columns);

        DoubleMatrix f = DoubleMatrix.zeros(H.columns);
        
        DoubleMatrix r = g.sub(H.mmul(f));
        
        DoubleMatrix p = H.transpose().mmul(r);

        int i = 0;

        do{
            DoubleMatrix alpha = r.transpose().mmul(r).div(
                p.transpose().mmul(p)
            );

            DoubleMatrix f1 = f.add(alpha.mmul(p));
            
            DoubleMatrix r1 = r.sub(alpha.mmul(H.mmul(p)));
            
            DoubleMatrix beta = r1.transpose().mmul(r1).div(
                r.transpose().mmul(r)
            );

            DoubleMatrix p1 = H.transpose().mmul(r1).add(beta.mmul(p));

            f = f1;
            r = r1;
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
