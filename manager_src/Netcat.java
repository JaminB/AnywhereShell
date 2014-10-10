/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package manager;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;


/**
 *
 * @author jamin
 */
public class Netcat {
    
    public int start() throws InterruptedException, IOException{
        if (Globals.os.toLowerCase().contains("win")){
            return this.startWindows();
        }
        else{
            return this.startLinux();
        }
    }
    public int startWindows() throws IOException, InterruptedException{
        return Runtime.getRuntime().exec(new Globals().scriptDir + "ncat_opener.bat").waitFor();
    }
    
    public int startLinux() throws IOException, InterruptedException{
        return Runtime.getRuntime().exec(new Globals().scriptDir + "nc_opener.sh").waitFor();
        
    }
}
