package Client;
import java.io.*;
import java.net.*;
import java.util.Queue;
import java.util.LinkedList;

class Server {
    public static Socket client;

    private static final Queue<Socket> filaDeRequisicoes = new LinkedList<>();

    public static void adicionarRequisicao(Socket client) {
        synchronized (filaDeRequisicoes) {
            filaDeRequisicoes.add(client);
            filaDeRequisicoes.notify();  // Notifica que há novas requisições
        }
    }


    private static void processarRequisicoesPendentes() {
        synchronized (filaDeRequisicoes) {
            if (!filaDeRequisicoes.isEmpty()) {
                Socket client = filaDeRequisicoes.poll();
                new Thread(new ClientHandler(client)).start();
            }
        }
    }


    public static void main(String[] args) {
        ServerSocket server = null;

        try {
            server = new ServerSocket(12000);
            server.setReuseAddress(true);

            // Monitorar Recursos
            SystemResourceObserver observer = new SystemResourceObserver();
            new Thread(observer).start();

            while(true) {
                client = server.accept();
                adicionarRequisicao(client);
                System.out.println("New client accepted: " + client.getInetAddress().getHostAddress());

                if (observer.getContinue()) {
                    processarRequisicoesPendentes();
                }

            }
        } catch (IOException e) {
            System.out.println("error");
        } finally {
            if (server != null) {
                try {
                    server.close();
                }
                catch (IOException e) {
                    System.out.println("error");
                }
            }
        }
    }


}