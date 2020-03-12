### p4ids - bmv2 version

We implement simple ip-block intrusion detection system(IDS). 
We build environment with 
* switch data plane (p4 code)
    * p4c (compile p4 code to p4-json)
    * bmv2 (runtime)
    * p4-utils (build runtime enviroment topology, map p4-json to runtime)
* switch control plane (controller)
    * p4controller (golang controller API)
* server, client
    * golang

#### Requirements
* [p4lang/p4c](https://github.com/p4lang/p4c)
* [p4lang/BMv2](https://github.com/p4lang/behavioral-model)
* [nsg-ethz/p4-utils](https://github.com/nsg-ethz/p4-utils)

#### How to run
1. in `src/p4/p4app.json`, change line 6 to path of switch executable
2. in `src/p4`, command:
> $ sudo p4run --config p4app.json
3. run controller, server, client sequentially
