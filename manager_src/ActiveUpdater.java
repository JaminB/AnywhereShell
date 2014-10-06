/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package manager;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author jamin
 */
public class ActiveUpdater {
    
    public String start(String ip, int port){
        String activeKnocks = new Client(Globals.serverIP, Globals.serverPort).getActiveKnocks();
        return activeKnocks;
      
    }
}
