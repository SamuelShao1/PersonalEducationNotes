
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
=
    3. Configuration Management

        * UseCase Property: Parsing the  UseCase property to determine the appropriate config settings

        * Configuration Commands: Setting various config parameters such as enable fields, tx-en, tx-power, and tfet mode.  

    4. Mode Settings

        * Transport Mode

        * Tfet Mode (Transmitter Fault/ Error Tolerance Mode), when enabled allows for modem to include error correction, such as retranmission of corrupted or last data. 
            
            * Enabled when transmission reliability is critical and to maintain data integrity in  scenarios where it is likely 

        * Streaming Mode is used for continious and real-time data transmission for applications that reqire a steady and consistent stream of data

            * Modem prioritizes low latenc and consistent data flow over fault tolerance

        * These modes relates to the modems operational modes

        * TX/RX modes when both enabled need to have different pins

## Testing Practices



## Corporate Interests / Values



## Resume Additional



## Talking Points



## Questions