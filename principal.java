//biblioteca blas: jblas
package Matriz;
import org.jblas.DoubleMatrix;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.Files;

import java.io.IOException;
import java.util.List;
import java.util.ArrayList;

public class Main {
	public static void main(String[] args){
		Path caminho = Paths.get("ArquivosCSV", "M.csv");
		Path caminho2 = Paths.get("ArquivosCSV", "N.csv");
		Path caminho3 = Paths.get("ArquivosCSV", "a.csv");
		
		List<String> dadosM = readCSV(caminho);
		List<String> dadosN = readCSV(caminho2);
		List<String> dadosA = readCSV(caminho3);

		DoubleMatrix M = convertToDoubleMatrix(dadosM);
        DoubleMatrix N = convertToDoubleMatrix(dadosN);
        DoubleMatrix a = convertToDoubleMatrix(dadosA);

        if (M.columns == N.rows) {
        	DoubleMatrix MN = M.mmul(N);
        	System.out.println("M * N:");
            printMatrix(MN);
        }
        
        if (a.columns == M.rows) {
        	DoubleMatrix aM = a.mmul(M);
        	System.out.println("a * M:");
            printMatrix(aM);
        }
        if (M.columns == a.rows) {
        	DoubleMatrix Ma = M.mmul(a);
        	System.out.println("M * a:");
            printMatrix(Ma);
        }
	}
	
	private static void printMatrix(DoubleMatrix matrix) {
        for (int i = 0; i < matrix.rows; i++) {
            for (int j = 0; j < matrix.columns; j++) {
                System.out.printf("%.0f ", matrix.get(i, j));
            }
            System.out.println(); 
        }
    }
	
	private static List<String> readCSV(Path caminho) {
		boolean existe = Files.exists(caminho);
		System.out.println("O arquivo existe? " + existe);
		System.out.println("PATH: " + caminho);
		
        if (existe) {
            try {
                List<String> conteudoDoArquivo = Files.readAllLines(caminho);
                return conteudoDoArquivo;
                
            } catch (IOException e) {
                System.err.println("Erro ao ler o arquivo: " + e.getMessage());
                
                return new ArrayList<>();
            }
        } else {
            System.out.println("O arquivo não foi encontrado no caminho especificado.");
  
            return new ArrayList<>();
        }
	}

	private static DoubleMatrix convertToDoubleMatrix(List<String> data) {
        int rows = data.size();
        int cols = data.get(0).split(";").length;
        DoubleMatrix matrix = new DoubleMatrix(rows, cols);

        for (int i = 0; i < rows; i++) {
            String[] values = data.get(i).split(";");
            for (int j = 0; j < cols; j++) {
                matrix.put(i, j, Double.parseDouble(values[j].trim()));
            }
        }
        return matrix;
    }
}
