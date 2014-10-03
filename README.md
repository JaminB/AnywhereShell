AnywhereShell
=============

Manage several remote machines without complicated firewall configurations. Works using reverse-tcp shells.

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

```
python negotiate.py
```
On your the computer you want to manage your agents from install xterminal and Java runtime environment 7 or above.

On the same computer move manager.jar and .knockrc to the same directory.
```
chmod +x manager.jar
*double-click to run* or java -jar manager.jar
```
On your router port-forward 9002 through to the host that has your management console running. This is neccessary so agents can connect back to you.

In the manager create knock "test."

On any computer you want to connect run the agent.
```
python agent -i $server_ip -k test
```
Simply click connect in the management-console using your knock: "test".
