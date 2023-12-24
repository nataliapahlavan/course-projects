/**
 * File: match-the-flag.js
 * -----------------------
 * Defines the controller for the MatchTheFlag application.
 */
"use strict";

function BootstrapMatchTheFlag() {
   let filenames = [];
   let clickedFlags = [];
   let twoFlagsClicked = false;

   // Iterates through the images folder to push the filnames by country
   for (let i = 0; i < NUM_COUNTRIES; i++) {
      filenames.push(`images/${COUNTRIES[i].toLowerCase()}.png`);
      filenames.push(`images/${COUNTRIES[i].toLowerCase()}.png`);
   }

   shuffle(filenames);

   let board = document.getElementById("board");
   let images = document.createElement("div");
   let coverImage = 'images/cover.png'

   // Creates the grid for the game
   for (let i = 0; i < filenames.length; i++) {
       let imageName = filenames[i];
       let imgNode = document.createElement("img");
       imgNode.setAttribute("src", coverImage);
       imgNode.setAttribute("data-country-image", imageName);
       imgNode.addEventListener("click", clickImage);
       images.appendChild(imgNode);  
   }

   board.appendChild(images);

   /*
    * Function: clickImage
    * -----------------
    * Responds to user's clicks. Keeps track of if the user has clicked two flags
    * and the name of the files of the clicked flags. If the user has clicked two
    * flags, then they are checked for a match.
    */
   function clickImage(e) {
      if (twoFlagsClicked) {
         return;
      }

      let imgNode = e.target;
      let current_src = imgNode.getAttribute("src");
      let originalFileName = imgNode.getAttribute("data-country-image");

      if (current_src === coverImage) {
         imgNode.setAttribute("src", originalFileName);
         clickedFlags.push(imgNode);
         if (clickedFlags.length === 2) {
            checkFlagMatches();
         }
      } else if (current_src !== MATCH_IMAGE) {
         imgNode.setAttribute("src", coverImage);
      }
   }

   /*
    * Function: checkFlagMatches
    * -----------------
    * If the user has clicked two flags, then they are checked for a match.
    * Waits a second before replacing the two image sources to be gray or transparent
    * using setTimeOut. Keeps track of if two flags are clicked and resets the clicked flags.
    */
   function checkFlagMatches() {
      if (clickedFlags.length == 2) {
         let [firstFlag, secondFlag] = clickedFlags;

         if (firstFlag.getAttribute("data-country-image") === secondFlag.getAttribute("data-country-image")) {
            setTimeout(function() {
               firstFlag.setAttribute("src", MATCHED_IMAGE);
               secondFlag.setAttribute("src", MATCHED_IMAGE);
            }, 1000);
         }
         else {
            twoFlagsClicked = true;
            setTimeout(function() {
               firstFlag.setAttribute("src", coverImage);
               secondFlag.setAttribute("src", coverImage);
               twoFlagsClicked = false;
            }, 1000);
         }
      }
      clickedFlags = [];
   }

   /*
    * Function: shuffle
    * -----------------
    * Generically shuffles the supplied array so
    * that any single permutation of the elements
    * is equally likely.
    */
   function shuffle(array) {
      for (let lh = 0; lh < array.length; lh++) {
         let rh = lh + Math.floor(Math.random() * (array.length - lh));
         let temp = array[rh];
         array[rh] = array[lh];
         array[lh] = temp;
      }    
   }
}

/* Execute the above function when the DOM tree is fully loaded. */
document.addEventListener("DOMContentLoaded", BootstrapMatchTheFlag);
