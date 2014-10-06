/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package manager;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

/**
 *
 * @author jamin
 */
public class Client {
    private String ip;
    private int port;
    
    public Client(String ip, int port){
        this.ip = ip;
        this.port = port;
    }
    
    public String createKnock(String knock){
        try {
            return this.send("> create: " + knock + " <");
        } catch (IOException ex) {
            return "Could not connect to server.";
        }
    }
    
    public String selectKnock(String knock){
        try {
            return this.send("> select: " + knock + " <");
        } catch (IOException ex) {
            return "Could not connect to server.";
        }
    }
    
     public String updateKnock(String knock, String status){
        try {
            System.out.println("> update: " + knock + " = " + status + " <");
            return this.send("> update: " + knock + " = " + status + " <");
        } catch (IOException ex) {
            return "Could not connect to server.";
        }
    }
     
     public String getActiveKnocks(){
        try {
            return this.send("> active <");
        } catch (IOException ex) {
            return "Could not connect to server.";
        }
    }
    
    private String send(String message) throws IOException{
        String response;
        Socket clientSocket;
        clientSocket = new Socket(this.ip, this.port);
        DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
        BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        outToServer.write(message.getBytes());
        response = inFromServer.readLine();
        clientSocket.close();
        return response;
        
    }
}
