/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package manager;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

/**
 *
 * @author jamin
 */
public class Globals {
    public String scriptDir;
    
    public Globals(){
        Parser parser = new Parser();
        parser.start();
        scriptDir = parser.scriptDirectory;
    }
    
    public void setScriptDirectory(String scriptDirectory){
        new Parser().setScriptDirectory(scriptDirectory);
    }
}

class Parser{
    private String configFile = Parser.class.getResource("knockrc").toString().replace("file:", "");
    
    //VARS
    public String scriptDirectory;
    
    public int start(){
        if (configFile.isEmpty() || configFile == null || configFile.trim().equals("rsrc:manager/knockrc")){
            configFile = "./.knockrc";
            System.out.println("Looking for config file in same directory: " + configFile);
        }
        String[] config = this.read().split("\n");
        for(int i = 0; i < config.length; i++){
            if (config[i].contains("=")){
                if (config[i].split("=").length > 1) {
                    String variable = config[i].split("=")[0];
                    String value = config[i].split("=")[1];
                    if (variable.toLowerCase().trim().equals("script_dir")){
                        this.scriptDirectory = value;
                        return 0;
                    }
                }
            }
            
        }
        return -1;
    }
    
    public int setScriptDirectory(String scriptDirectory){
        this.start();
        String raw = this.read();
        if(raw.contains("script_dir")){
            return this.write(raw.replace(this.scriptDirectory, scriptDirectory));
        }
        else{
            return this.write(raw + "\n" + "script_dir=" + scriptDirectory);
        }
    }
    
    public String read(){
        String totalLines = "";
        try (BufferedReader br = new BufferedReader(new FileReader(configFile)))
		{
                        
			String line;
			while ((line = br.readLine()) != null) {
				totalLines += line;
			}
 
		} catch (IOException e) {
			return "failure";
		} 
        return totalLines;
    }
    public int write(String value){
        FileWriter fstream;
        try {
            fstream = new FileWriter(configFile);
        } catch (IOException ex) {
            return -1;
        }
        BufferedWriter out = new BufferedWriter(fstream);
        try {
            out.write(value);
        } catch (IOException ex) {
            return -1;
        }
        try {
            out.close();
        } catch (IOException ex) {
            return -1;
        }
        return 0;
    }
}

