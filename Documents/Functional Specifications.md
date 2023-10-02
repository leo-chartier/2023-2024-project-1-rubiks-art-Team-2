# Rubik's art

<details>
<summary>Table of Contents</summary>

- [Rubik's art](#rubiks-art)
  - [Overview](#overview)
  - [Stakeholders](#stakeholders)
  - [Scope](#scope)
  - [Personas and use cases](#personas-and-use-cases)
  - [Evaluation criteria](#evaluation-criteria)
  - [Proposed designs](#proposed-designs)
    - [Selected solution](#selected-solution)
    - [Test phase](#test-phase)
  - [Risks and assumptions](#risks-and-assumptions)
  - [Non-functional requirements](#non-functional-requirements)
  - [Maintaining](#maintaining)
  - [Glossary](#glossary)

</details>

---



## Overview

ALGOSUP is looking for someone to produce a 60-100 square feet (5.57-9.29 square meter) fresco entirely made of Rubik’s cubes.  
The fresco will be a permanent feature of the school, displayed in what is currently the library and visible from the outside.

Each cube is to be treated as a 3x3 [pixel](#pixel) [matrix](#matrix) with each panel being a [pixel](#pixel) of either green, yellow, red, orange, blue or white color.  
The library may have to be rearranged or moved in order to make the fresco more visible.

## Stakeholders 

|                                                   Profile                                                    | Name & link                                                | Description    |
| :----------------------------------------------------------------------------------------------------------: | ---------------------------------------------------------- | -------------- |
|            <img alt="ALGOSUP" src="https://avatars.githubusercontent.com/u/69455243" width="30">             | [ALGOSUP](https://www.algosup.com/)                        | Client company |
|    <img alt="Lucas Aubard" src="https://gravatar.com/avatar/dc3a8fc938e413abe9fb0053201896e7" width="30">    | [Lucas AUBARD](https://github.com/LucasAub)                | Team member    |
|        <img alt="Documents/VivienBistrelTSANGUECHOUNGOU" src="https://avatars.githubusercontent.com/u/122369054" width="30">         | [Vivien BISTREL](https://github.com/Bistrel2002)           | Team member    |
|    <img alt="Léo Chartier" src="https://gravatar.com/avatar/c8a06da2c80a003656e90ab4afa49ea8" width="30">    | [Léo CHARTIER](https://github.com/leo-chartier)            | Team member    |
|  <img alt="Quentin Clément" src="https://gravatar.com/avatar/a8f1bb3cfa42b20d11fb6ddcc9ac5bdf" width="30">   | [Quentin CLÉMENT](https://github.com/Quentin-Clement)      | Team member    |
| <img alt="Aurélien Fernandez" src="https://gravatar.com/avatar/4a7908c1162aa68cbf3c8c06edc7053d" width="30"> | [Aurélien Fernandez](https://github.com/aurelienfernandez) | Team member    |
|  <img alt="Thomas Planchard" src="https://gravatar.com/avatar/e73464278d5fb76a24b77a7d79bf39ba" width="30">  | [Thomas Planchard](https://github.com/thomas-planchard)    | Team member    |
|                   <img alt="Student" src="https://gravatar.com/avatar/0?d=mp" width="30">                    | Students and other building employees                      | End user       |
|                  <img alt="Passer-by" src="https://gravatar.com/avatar/0?d=mp" width="30">                   | Passer-by                                                  | End user       |


## Scope

The main objective is to create a fresco that is both accepted by ALGOSUP and eye-pleasing.

## Personas and use cases

**1 Curious Citizen of Vierzon - Yves**

*Background:*
Yves is a 56-year-old long-time resident of Vierzon, known for frequently strolling down the "rue de la société française." He has two children: a 17-year-old daughter and a 15-year-old son.

*Goals and Objectives:*
Yves is curious about the world around him and often seeks out new experiences and information. He values education and wants the best for his children's future.

*Challenges:*
Yves is unfamiliar with the schools in the city and is looking for a reliable educational institution that can offer quality education for his children.

*Scenario:*
If Yves encounters the fresco every day on his way down the "rue de la société française," he will notice ALGOSUP's name. This may pique his curiosity, leading him to search for more information about the school. Yves is the kind of person who actively engages with his community, and when he discovers something interesting, he shares it with his children.

*Impact:*
If Yves learns about ALGOSUP and finds it appealing, he may discuss it with his children. This could potentially lead one of them to share the information with their friends or even consider joining ALGOSUP for their education. Yves' curiosity and engagement with his community could have a positive ripple effect, potentially increasing awareness and interest in the school.

**2. Art Enthusiast - Emily**

*Background:*
Emily is a 25-year-old student with a passion for unconventional mediums. She thrives on creative challenges and has experience in working with various materials.

*Goals and Objectives:*
Emily aims to create a visually striking and thought-provoking fresco that not only meets ALGOSUP’s requirements but also showcases her artistic talent.

*Challenges:*
Balancing artistic expression with technical constraints, and ensuring that the final piece effectively represents ALGOSUP's identity.

**3. Engineering Enthusiast - Alex**

*Background:*
Alex, 28, is an student with a keen interest in robotics and mechanical systems. He is excited about the opportunity to combine his technical skills with artistic expression.

*Goals and Objectives:*
Alex wants to leverage technology to optimize the cube rotations and assembly process, ensuring precision and efficiency in the creation of the fresco.

*Challenges:*
Designing a mechanical system that can seamlessly integrate with the artistic vision and coordinating with the artistic team to implement rotations effectively.


## Evaluation criteria 
The fresco will be a permanent feature in the school's library, serving as a visual representation of ALGOSUP's identity. It will encompass the following key elements:

- **ALGOSUP’s Logo:** The logo will be prominently featured as a central element of the design, representing the core identity of ALGOSUP.

- **Evocation of ALGOSUP’s Building:** The fresco will incorporate artistic elements that evoke the architectural characteristics of ALGOSUP's building, providing a unique connection between the artwork and the institution.

- **Color Palette:** The fresco will use a vibrant color palette derived from the Rubik's cube facets, including green, yellow, red, orange, blue, and white.

- **Text (Optional):** If included, any textual elements will be in English and will complement the overall design, conveying a message aligned with ALGOSUP’s values.

- **3. Dimensions and Layout:**
The fresco will be rectangular in shape, occupying an area between 60-100 square feet. The layout will be designed to maximize visibility from both the interior of the library and the exterior of the building.

- **4. Cubes Utilization:**
The design will incorporate a minimum of 2000 and a maximum of 3000 Rubik's cubes. Each cube will be treated as a 3x3 pixel matrix, with no disassembly allowed.

- **5. Cube Rotation and Positioning:**
All cubes will be rotated into position to create the desired artistic composition. Sequences of cube rotations will be recorded for documentation and social media content.


Additionally, recording of the construction must be provided in the form of a video or timelapse for the school's social media. 

## Proposed designs

1.  Some point on the evaluation criteria above will be taken into account when designing the fresco, all proposal on the designing face shall be done by the team members, and the final design have to be approve by all the members. 
2.  An image software will be used to design fresco so that it matches with the desire number of rubiks cube.
### Selected solution
<img alt="ALGOSUP" src="./../Images/SelectedFresco.png" width="300"> 

This image is the fresco selected by the entierety of our team. We choose this solution for it's simplicity, this view of the building show how important are ALGOSUP's roots within the city of Vierzon. Moreover, on the bottom left, you can see a QR code, this code redirect directly to ALGOSUP's official website.

### Test phase
<img alt="ALGOSUP" src="./../Images/Unselected1.png" width="200"> 
<img alt="ALGOSUP" src="./../Images/Unselected2.png" width="200"> 
<img alt="ALGOSUP" src="./../Images/Unselected3.png" width="200"> 
<img alt="ALGOSUP" src="./../Images/Unselected4.png" width="200"> 

During the research process we experimented a few design. As you can see they weren't very eye-pleasing. The first image shows how colors could be saturated by using strong colors without balancing the image's colors properly. The following images are showing how white, green and yellow could make the image unreadable for the eye. Taking this into consideration, we choosed to avoid green and yellow, and use far less white.

We also thought of creating a two-faced fresco, for people outside of the school and for the students and the staff. However we quickly found that the time required and the difficulty of such task is greater than what we can realistically offer.

## Risks and assumptions

The main risk of the project is, not succeding in the creation of a well presentable pixel image containing the needed interval of rubik cubes, as such a software program will be use for the creation of a pixel image, that originate from a real image while considering the fact that one image pixel is the same as one cube pixel. 

## Non-functional requirements

We have few to none non-functional requirements, the main one is the QR code disposed on the bottom left of the fresco, as previously mentioned, the QR code is redirecting on ALGOSUP's official website.

## Maintaining

The maintenance is an essential part of every project, particulary with artistic projects. The fresco will need to be properly cleaned to keep the image visible. The fresco might also be destroyed or small parts can be disasembled by accident, to overcome this, a member of the group will have to visit the fresco during each breaks to see if a part is missing or on the ground.

As for the cleaning, a quick wipe should suffice to clean the dust from the cubes.


## Glossary
<span id="matrix">Matrix</span>: A rectangular table of quantities or expressions in rows and columns that is treated as a single entity and manipulated according to particular rules.

<span id="pixel">Pixel</span>: the smallest unit of an image on a television or computer screen

