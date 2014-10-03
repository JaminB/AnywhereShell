AnywhereShell
=============

Easily manage your reverse-shells by assigning "knocks" to each.

Protocol
=============
The negotiation server is used to register different "knocks" to agents. These knocks are used to identify individual agents. The agent is the assigned a knock that is registered to the negotiation server. When the management console is ready to connect to the agent it tells the negotiation server to set the knock status for that agent from "wait" to "connect." The agent then connects outbound to the management console.


                    > Negotiation-Server <
                   /                      \
                  /                        \
                agent -------------> management-console

Usage
=============
Currently only works on Linux!


Start the negotiation server on an external VPS. It must be public facing!

```
python negotiate.py
```
Make sure that there is a knock directory in the same directory as negotiate.py. This is where the knocks get stored.

```
touch knocks
```

On your the computer you want to manage your agents from install xterminal and Java runtime environment 7 or above.

On the same computer move manager.jar and .knockrc to the same directory.
```
chmod +x manager.jar
*double-click to run* or java -jar manager.jar
```
Put the scripts somewhere on your file-system. In the manager config tab browse for the script directory, and click apply.

On your router port-forward 9002 through to the host that has your management console running. This is neccessary so agents can connect back to you.


In the manager create knock "test."

On any computer you want to connect run the agent.
```
python agent -i $server_ip -k test
```

Simply click connect in the management-console using your knock: "test".
