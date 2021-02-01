# ComicOrchard
Organizational tool and library designed for comic books

This Program Was Written by Nick Burbach and Gianni Young

Digital Comic book metadata is inconsistent to say the least. There is no real standard and there is no gaurentee that a file containing metadata exists within the comic. Our goal with this project was to use the closest thing to standard when it comes to comic book metadata; ComicRack tags. While the information contained within this format is fine, the issue lies with its adoption and ability to be generated. Comic books are more complex than many realize and are often inconsistent in there own ways. ComicVine is the closest thing there is to a complete comic database but it has a poorly managed and maintained api and often houses incomplete metadata. Our ultimate goal for this project was to be able to sort comics by story arcs, characters, and any other metadata. This goal was only partially fulfilled because on ComicVine storyarcs are linked to comics but not the other way around. This issue made it significantly harder than anticipated. We settled for sorting upon the metadata that was most readily available.

Our program uses an sqlite database as a background and is written in python. The features in our program include the ability to sort comics upon various metadata. Open a selected comic with mcomix. Import a collection of comics. Import a single comic. As well as the ability to remove a single or multiple comics if desired. At the top we have implemented a search bar that allows a user to filter for a specific word or phrase amongst all of our metadata.



![Image of Comic Orchard](https://github.com/GianniBYoung/blob/main/ComicOrchard/Comic_Orchard.png?raw=true)
