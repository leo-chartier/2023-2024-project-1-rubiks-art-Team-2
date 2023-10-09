# Rubik's art

<details>
<summary>Table of Contents</summary>

- [Rubik's art](#rubiks-art)
  - [Introduction](#introduction)
  - [Design Details](#design-details)
    - [Fresco Dimensions](#fresco-dimensions)
    - [Cube Representation](#cube-representation)
    - [Cube Arrangement](#cube-arrangement)
    - [Mounting and Display](#mounting-and-display)
    - [Protective Measures](#protective-measures)
    - [Construction Process](#construction-process)
  - [Maintenance and Upkeep](#maintenance-and-upkeep)
  - [Documentation and Reproduction](#documentation-and-reproduction)
  - [Fresco support](#fresco-support)
  - [Technology used](#technology-used)
  - [Assumptions](#assumptions)
  - [Pros and Cons](#pros-and-cons)
  - [Security Considerations](#security-considerations)
  - [Risks](#risks)
  - [Success Evaluation](#success-evaluation)
  - [Conclusion](#conclusion)
  - [Glossary](#glossary)

</details>

---

## Introduction

The Rubik's Art Fresco is a permanent artwork commissioned by ALGOSUP, consisting of Rubik's cubes arranged to form a pixelated image representing the institution. This technical specification outlines the detailed implementation plan for the creation, installation, and maintenance of the fresco.


##  Design Details

###  Fresco Dimensions

- Area: 9.3≈  square meter 
- Rectangular shape to maximize visibility(184.8cm x 504cm)

###  Cube Representation

- Each Rubik's cube represents a 3x3 pixel matrix.
- Colors: Green, Yellow, Red, Orange, Blue, White.

###  Cube Arrangement

- The design will be composed of 2970 Rubik's cubes. (90x33)
- Cubes will be precisely rotated and positioned to create the desired artistic composition.

###  Mounting and Display

- The fresco will be placed on a plank securely attached to the wall over the sockets to prevent accidental displacement.
- A clear acrylic panel will be installed in front of the cubes to offer protection and reduce maintenance needs.

###  Protective Measures

- The mounting structure will be designed to minimize stress on the cubes.
- Periodic inspections will be conducted to ensure the structural integrity and stability of the fresco.



### Construction Process
ALGOSUP's students are divided in 8 project teams. When the final image will be chosen by the client, each team will have to collaborate to realize the final fresco. Even so, each one will have to work on their on under the control of the chosen team.

If chosen, Team 2 will primarily handle the organization and execution of the construction process.

Tasks will be divided into small, manageable blocks for easy distribution.

As you can see below, we divided our image in 36 sections:
- 30 sections of 90 rubik’s cube (15 width x 6 height)
- 6 sections of 45 rubik’s cube (15 width x 3 width)

<img alt="division" src="./../Images/Tasks_division.png" width="600">


Each team will be assigned specific sections to construct. This division of labor into 36 sections will enable us to tailor the workload to each team's pace.

Simultaneously, our team will focus on designing, developing, and building the support structure for the fresco.

Furthermore, each team will receive a detailed plan outlining their specific responsibilities, including the placement of Rubik's cubes within their assigned section. This plan will serve as a guide, ensuring accurate execution.

Additionally, to bolster team comprehension and guarantee precise execution, we will employ a specialized software program that visually illustrates the various potential movements of the Rubik's cubes.



## Maintenance and Upkeep

- Regular cleaning of the acrylic panel to maintain visibility. At least once a week.
- Routine inspections to identify any missing or damaged cubes, with prompt replacement.
- Any necessary repairs or replacements will be performed promptly to ensure the longevity of the artwork.



##  Documentation and Reproduction

- A comprehensive document will be provided detailing the construction process, including cube rotations and arrangements.
- This documentation will serve as a reference for maintenance, reproduction, or any potential future modifications.
  



## Fresco support

To support our fresco, we chose to place it on a plank which is on the plugs and screw it to the wall to reinforce the structure.....

## Technology used 

We created a prototype robot to help us with the rotation of the Rubik's cubes as it is much faster than a human. Because of logistical constraints and time considerations, we decided not to keep on using this robot for the actual construction. Indeed, the communication system with the robot is new to us and learning to use it would take too much time and the incorporation of its usage in parallel to the other teams is too much of a burden.

Furthermore, a software developed in Python has been created to distribute the tasks between the teams and help with the actions to take. The reason for this choice is based on the fact that we will be using a Google Spreadsheet to keep track of the work, its API being accessible in Python. Also, to incorporate external websites, Python is a good alternative to Google's AppScripts which does not implements all the classic methods of a website.

## Assumptions
It is assumed that the provided Rubik's cubes will be of standard size and quality, and no significant defects will be encountered during the construction process.
The provided image overlay will accurately represent the desired final result.

## Pros and Cons
Pros:

The Rubik's Art Fresco offers a visually captivating representation of ALGOSUP's identity.
The use of Rubik's cubes provides a unique and engaging artistic medium.

Cons:

The construction process may be labor-intensive and time-consuming, particularly if a significant number of cubes are deemed unusable.

## Security Considerations
The mounting structure will be designed to minimize stress on the cubes and prevent accidental displacement.
The clear acrylic panel will offer an additional layer of protection and reduce maintenance needs.

## Risks
The main risk lies in the potential difficulty of creating a pixelated image using Rubik's cubes within the specified cube count range.
To mitigate this, a software program will assist in generating instructions for the construction process.

## Success Evaluation
The success of the project will be determined by the feedback provided by the daily workers of the B3, as well as the degree of similarity between the final image and the original prototype. This evaluation will serve as a crucial indicator of the project's overall success and alignment with the intended vision.


## Conclusion
By adhering to these technical specifications, we aim to create a Rubik's Art Fresco that not only meets ALGOSUP's vision but also stands as a durable and visually captivating representation of the institution's identity.

## Glossary 


