
# Ciena Crib Sheet

## Preliminary Vocabulary

* Modem: A modulation devices that converts digital data from computers or other devices into
analog signals that can be transmitted along analog mediums such as phone lines, fiber optics, celluar networks. 



## Ciena Wave Logic Optical Modem

* High performance fiber optical modem for scalable and flexible data transmission

* Features:
    * 400G (Gbps) per wavelength with scaling potential

    * QAM modulation schemes, optimizing balance between capacity and reach

    * Programmable modulation, ability to be adjusted to match distance and route requirements

    * Forward Error Correction FEC

        * Uses encoded redundant bits to decode and correct corrupted data

    * Uses adaptive (Digital signal processing) DSP alogs to optimize performance 

    * Network automation by integrating with Ciena's network automation and management orchestration
    tools

* Applications

    * Data Center Interconnects DCI (High capacity links between data centers and cloud services and large-scale data storage)

* Relationship to the Application Test

    1. Modulation and Signal Processing

        * DS/EN Interface: Test involves enabling and disabling client interface, which is related to modem modulate and demodulate signals

        * Laser Frequency: Crucial component for optical signal transmission

            * Determines the wavelength of light used to tranmit data, and is crucial to match the characteristics of the optical fiber for efficient data transmissionwha

        * TX (Transmit) and RX (Recieve) paths

    2. Data Rates and Capacity

        * Speed Rating: Configuring the speed mode for both transmit and receive which involves setting data transmission rates (600GB, 1200GB...)

        * Pin Configuration: Allocating seredes pins based on speed rating, reflecting how modem handles high-capacity data transmission


    3. Configuration Management

        * UseCase Property: Parsing the  UseCase property to determine the appropriate config settings

        * Configuration Commands: Setting various config parameters such as enable fields, tx-en, tx-power, and tfet mode.  

    4. Mode Settings

        * Tfet Mode (Transmitter Fault/ Error Tolerance Mode), when enabled allows for modem to include error correction, such as retranmission of corrupted or last data. 
            
            * Enabled when transmission reliability is critical and to maintain data integrity in  scenarios where it is likely 

        * Streaming Mode is used for continious and real-time data transmission for applications that reqire a steady and consistent stream of data

            * Modem prioritizes low latency and consistent data flow over fault tolerance

        * These modes relates to the modems operational modes

        * TX/RX modes when both enabled need to have different pins

## Experience with optical technology and photonics

### Optical Technology

* WDM Wavelength Division Multiplexing: Technology used to transmit multiple signals at the same time on different wavelenghts of light within the same optical fiber

    * Things to consider for testing: Channel Spacing, signal integrity, performance

### Photonics

* Ciena WLModem uses PIC providing integrated miniaturization of components

* Use technologies such as QAM and Phase Shift Keying PSK for high data rates and efficient use of optical spectrum. 

    * Techniques used to detect the phase and amplitude of light waves is called COHERENT DETECTION

* Optical Signal Processing

    * DSP used in conjunction with photonics to compensate for impairments such as dispersion

### In relation to testing:

* Testing Quality: 
    * Bit/Data errors: Sending a sequence of bits through the modem and comparing the received      sequence to the transmitted sequence for discrepencies
    
        * Jitter: Variability in time domain of signals transitions (voltage changes), leading to timing errors and data corruption, synch issues, especially important for streaming

        * Noise: Variations in signals that can distort data. 


* Testing Single vs Multi Fiber: Consider dispersion

* Quality among various transport modes

    * Short haul Data Centers

        * Shorter distances, higher data

        * Focus on maintain error rate

        * Example Test: Various buildings within a campus or city, Large datasets 800Gbps, 800LR transceiver, 10km

        * DATA CENTERS considerations

            * High Data thoroughput (data rates)

            * Low latency (to support real-time applications and services)

            * High availibility: Redundancy and failover mechanisms

    * Long haul (such as telecom networks)

        * Depending on the distance:

            * 120km: Could add an amplifier to still provide 800G (aka 800ZeroDispersion transciever)

            * 1000km: 800G default

            * 400G for pluggabble very long distances

        * Example Test: 800 Gigabits via , 1000km

        * More sucesptible to signal attenuation, dispersion, noise

        * Use amplification, dispersion compensation sycg as Digital Signal Processing DSP

            * This could lead to malformation of the sequence in the process?

    * To mimic long distances we could have a loopback between a series of network paths

## Testing Practices

* Unit Testing: Individual components or functions in solation

* Integration: Testing integrated units or components

* System: Integrated software, user interaction

* Use virtual networks to mimic long distances, adding data errors, in order to test how the modem can either amplify, forward correct, or use optical signal processing/DSP to fix or manage errors. Reduces wait time for retrival of data. Though we would need an aggreagted data set from real world data for accuracy, but could also see how we can push the modem's technologies regardless. (because amplification and error-correction is still all software)

* STLC

    1. Requirement analysis, tracebility matrix

    2. Test planning and strategies

    3. Case development or test dev

    4. Enviroment, ie the network, or virtual network, and associated hardware

    5. Execution then conclusion

### Testing Techniques

* Black Box: Abstract the function as a empty box, you know nothing about the internals of the application, only know what inputs and expected outputs

* White Box: Opposite, Examples: Coverage analysis, path testing, unit testing

* Gray Box: Partial knowledge, for integration testing and component interaction (Photonic integrated circuit)

* Methodolgies

    * Waterfall: Linear phases, can't go back so ridgit

    * V-Model: Each dev phase will have test phase

    * Agile/Scrum: Iterative, incremental, emphasizes flexiility and customer satisfaction

* CI/CD: 

    * Integrates code frequently and runs automated tests at every integration aligns well with agile, but can be with other methodologies

    * Working copies are merged/commited several times a day, aims to address integration issues multiple times a day


### Keyword brush ups

* Modems use IP to assign addresses to devices and route traffic to and from the internet

    * IP4: 32bit, 4 billion addresses

    * IP6 128bit much much more

    * Subnetting 

* Ethernet uses mac to identify recipent/sender


* TCP/IP: Protocols use to interconnect network devices on the internent

    * TCP insures reliable data transmission and IP handles addressing and routing

        * Establishes connection before data transfer to ensure reliability

        * Manages data transfer rates

        * HTTP, HTTPS

    * UDP connectionless, data is just sent

        * Unreliable but lower overhead

        * DNS, streaming

* Switching: Aka data forwarding of data packets, and they operate at the link layer (layer 2) of the OSI model

    * Modem may have multiple ethernet ports with switching functionality

* VLANs: Segregates network traffic for security. Uses tags to idenfity vlans at the ethernet port frames. 

* SDKs include ciena's APIs

* SDNs: EVPN uses BGP overlay to share VRF tables to provide ethernet multipoint, allows seemless interconnection between various DCInterconnects. Because it uses BGP is allows for high scalability. VLAN is only layer 2, where was VXLAN as a layer 2 overlay on layer 3, and BGP provides 2/3 layer services with integrated routing and briding

    * Use EVPN for connection multiple seasmless VM mobility and redundacy

    * VXLAN for extensive network segmentation beyond VLAN and creating isolated virtual networks within multi tenant cloud enviroments'

    * EVPN for integrating on premis and cloud enviroments

    * Proxmox actually uses a EVPN-VXLAN-BGP based SDN

        * BGP as a control plane for mac address learning and VRF ip sharing between datacenters (layer 3) and inter-dc (layer2) -> redundacy, seamless traffic

        * Prox then uses VXLAN tunnels between nodes/servers and network devices (VTEPs) for layer 2 over layer 3 for data transport by encapusilating the ethernet frames. Basically VXLAN has the dataplane and BGP for the controller plane or routing.

## Resume Additional

* NORTHROP GRUMMAN

    * Part of the mission systems divison of NGC, that supports cyber and software solutions for situational awareness. Within that I worked with the R&D team at the branch in San Antonio.

    * I had a couple a roles and tasks here but my main project involved configuring and automating an SDN on a type 1 hypervisor, Proxmox (similar to VMWare ESXI) that would hosts the VM and containers, etc for the various research and development project groups within this location. and the purpose of the SDN would provide multi-tenancy while maintain network isolation and seamless data transfer between nodes/servers. And ultimately we would then connect our local R&D network two the larger company wide unclassed developemnet network. So the project can be broken down into two main facets. 

        * The first part of this project involved configuring the virt enviroment with a software defined network based on EVPN technology that used BGP as a controller plane for routing, such as sharing vrf (virt rout) tables and mac addresses. Then the EVPN SDN also used a layer 2 overlay using VXLAN tunnels or VTEPs to provide a data plane for encapusilating data transportation on the ethernet ports. Ultimately we wanted to create a ne
            
            *The BGP controller had two parts.  VYOS
            * Other: Non-traditional in a sense because my mentor wasn't a Network or System engineer but a software engineer. In fact, there were no network engineers consistently based at our location and the systems engineers were on classfied programs. This meant I had to do a lot of research and bounce ideas back and forth with my mentor as he wasn't always comepletely sure the steps to take. It allowed me to can test and explore what worked and solutions to implement.

        * The second part of the project involved creating an automation script to onboard the tenants. The if a client or tenant came up to use and wanted to create a dev enviroment. The script would automatically spin up a isolated evpn zone. The script then creates permission groups to inforce limits on the tenant, such as the amount of VMs that can be created, where the VMs could be created, its subnet and gateway addresses, and resource limitations. This was done mainly in python, where I made API requests to the host server to do most of the configuration. However, some parts couldn't be implemented using the API such as allocating resources or user creation so I used a combination of paramiko SSH shells and CLI commands. 

        * Other things like setting up the GitLab repository, the runner for CICD etc


* GOOGLE
    * I worked with UI/UX clients at Google to create an web application for anaylzing and sentiment and thematic context of user-research survery, so this is obviously a very client facing role. I would say we followed a Agile/scrum metholody here though more rigid due to requirements of the capstone course, but with each Sprint we conducted continous feedback from our clients as well as user survey. 

    * The frontend consist of a TS CSS while the backend incliuded python and Gemeni API which we then tuned. The previous itertion was using Bard. 

    * Embeddings 

        * Collected our data and pushed it through a data preporcess pipeline to from both research surveys as well as client examples. Used gemeni to generate the embeddings, then we use a KMeans clustering algo to group similar texts into themes. 

            * KMEANs because we had a predefined set of themes given to us by the client

* GTRI

    * Robotics + Arduino used Pixy Camera 

        * Previous algo used RRT

        * Implemented Astar which was much much better and allowed for bi-dirctionality
## Talking Points



## Questions

* What will work be like? Implementing/completeing tickets, or if you guys do CICD creating pipelines?

    * Groups? Following waterfall/other metholodogy?

* Format of internship: hybrid? 

* Clearance needs ? Saw other posting for a full time


Coherent Detection: QAM

Definition: Coherent detection involves using a local oscillator laser at the receiver to mix with the incoming optical signal. This technique enables the extraction of both the amplitude and phase information of the signal.