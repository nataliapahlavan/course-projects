/*
 * File: Enigma.js
 * ---------------
 * This program implements a graphical simulation of the Enigma machine.
 */

"use strict";

/* Main program */

function Enigma() {
	let enigmaImage = GImage("EnigmaTopView.png");
	enigmaImage.addEventListener("load", function() {
		let gw = GWindow(enigmaImage.getWidth(), enigmaImage.getHeight());
		gw.add(enigmaImage);
		runEnigmaSimulation(gw);
   });
}

// You are responsible for filling in the rest of the code.  Your
// implementation of runEnigmaSimulation should perform the
// following operations:
//
// 1. Create an object that encapsulates the state of the Enigma machine.
// 2. Create and add graphical objects that sit on top of the image.
// 3. Add listeners that forward mouse events to those objects.

/* Function: runEnigmaSimulation */
// Runs the Enigma machine that was used during World War II to encode messages
function runEnigmaSimulation(gw) {
   let enigma = {
   	lamps: [],
   	rotors: [],
   	permutations: [],
   	inversePermutations: []
   };
   let x0 = 0;
   let y0 = 0;

   /* Function: locationToLampLetter */
   // Takes the x and y coordinates of the key location and returns the index of the letter in the alphabet
   function locationToLampLetter(x, y) {
   	for (let i = 0; i < KEY_LOCATIONS.length; i++) {
   		if (KEY_LOCATIONS[i].x == x && KEY_LOCATIONS[i].y == y) {
   			return i;
   		}
   	}
   }

   /* Function: createKey */
   // Creates the keys at the bottom of the GWindow. First, a circle is created and placed at the locations given
   // by KEY_LOCATIONS and the key's label is added on top of the circle.
   function createKey() {
   	for (let i = 0; i < KEY_LOCATIONS.length; i++) {
   		let key = GCompound();
   		let circle = GOval(KEY_LOCATIONS[i].x - KEY_RADIUS, KEY_LOCATIONS[i].y - KEY_RADIUS, KEY_RADIUS * 2, KEY_RADIUS * 2);
   		circle.setFilled(true);
   		circle.setColor(KEY_BORDER_COLOR);
   		circle.setFillColor(KEY_BGCOLOR);
   		circle.setLineWidth(KEY_BORDER);
   		key.add(circle);
   	// Create the letter that appears inside the circle
   		let keyLabel = new GLabel(ALPHABET[i], KEY_LOCATIONS[i].x, KEY_LOCATIONS[i].y);
   		keyLabel.setFont(KEY_FONT);
			keyLabel.setColor(KEY_UP_COLOR);
			keyLabel.setTextAlign("center");
			keyLabel.setBaseline("middle");
			key.add(keyLabel);
			gw.add(key);

		// Advances the fast rotors every time a key is clicked. When the fast rotor returns back to its original index ("A" or 0),
		// the medium rotor begins advancing, then the slow rotor.
   	key.mouseDownAction = function(enigma) {
   		keyLabel.setColor(KEY_DOWN_COLOR);
   		
   		let x = keyLabel.getX();
   		let y = keyLabel.getY();
   		let permLetter = locationToLampLetter(x, y);

   		if (advanceRotor(enigma.rotors[2])) {
      		if (advanceRotor(enigma.rotors[1])) {
      			advanceRotor(enigma.rotors[0]);
      		}
      	}

      	// Completes the forward permutation (fast, medium, then slow)
   		for (let j = 2; j >= 0; j--) {
   			permLetter = applyPermutation(permLetter, enigma.permutations[j], enigma.rotors[j].offset);
   		}

   		permLetter = applyPermutation(permLetter, REFLECTOR_PERMUTATION, 0);

   		// Completes the inverse permutation (slow, medium, then fast)
   		for (let j = 0; j <= 2; j++) {
   			permLetter = applyPermutation(permLetter, enigma.inversePermutations[j], enigma.rotors[j].offset);
   		}

   		enigma.lamps[permLetter].label.setColor(LAMP_ON_COLOR);
   	}

   	// Similar to mouseDownAction, this function applies the forward and inverse permutations
   	key.mouseUpAction = function(enigma) {
   		keyLabel.setColor(KEY_UP_COLOR);
   		let x = keyLabel.getX();
   		let y = keyLabel.getY();
   		let permLetter = locationToLampLetter(x, y);
  
   		for (let j = 2; j >= 0; j--) {
   			permLetter = applyPermutation(permLetter, enigma.permutations[j], enigma.rotors[j].offset);
   		}
   		permLetter = applyPermutation(permLetter, REFLECTOR_PERMUTATION, 0);
   		for (let j = 0; j <= 2; j++) {
   			permLetter = applyPermutation(permLetter, enigma.inversePermutations[j], enigma.rotors[j].offset);
   		}
   		enigma.lamps[permLetter].label.setColor(LAMP_OFF_COLOR);
   	}
   	}
	}
   createKey();

   /* Function: mouseDownAction */
   // Finds the object that exists at a certain location and then ignores the event or complete a function depending
   // on if the object is null or not
   function mouseDownAction(e) {
   	 let object = gw.getElementAt(e.getX(), e.getY());
   	 if (object !== null && object.mouseDownAction !== undefined) {
   	 	object.mouseDownAction(enigma);
   	 }
   };

   /* Function: mouseUpAction */
   // Finds the object that exists at a certain location and then ignores the event or complete a function depending
   // on if the object is null or not
   function mouseUpAction(e) {
   	let object = gw.getElementAt(e.getX(), e.getY());
   	if (object !== null && object.mouseUpAction !== undefined) {
   		object.mouseUpAction(enigma);
   	}
   };
   
   /* Function: createLamp */
   // This function creates the lamps that are above the keys. A lamp circle is created and then a label is added on
   // top of the circle. 
   function createLamp() {
   	for (let i = 0; i < LAMP_LOCATIONS.length; i++) {
   		let lamp = GCompound();
   		let lampCircle = GOval(LAMP_LOCATIONS[i].x - KEY_RADIUS, LAMP_LOCATIONS[i].y - KEY_RADIUS, KEY_RADIUS * 2, KEY_RADIUS * 2);
   		lampCircle.setFilled(true);
   		lampCircle.setColor(LAMP_BORDER_COLOR);
   		lampCircle.setLineWidth(KEY_BORDER);
   		lamp.add(lampCircle);
   	// Create the letter that appears inside the circle
   		let label = new GLabel(ALPHABET[i], LAMP_LOCATIONS[i].x, LAMP_LOCATIONS[i].y);
   		lamp.label = label;
   		label.setFont(LAMP_FONT);
			lamp.label.setColor(LAMP_OFF_COLOR); 
			label.setTextAlign("center");
			label.setBaseline("middle");
			lamp.add(label);
			gw.add(lamp);

			// Lights up the color of the label if a mouseDownAction occurs
			label.mouseDownAction = function(enigma) {
				label.setColor(LAMP_ON_COLOR);
			}

			// Turns the color of the label off if a mouseUpAction occurs
			label.mouseUpAction = function(enigma) {
				label.setColor(LAMP_OFF_COLOR);
			}
			enigma.lamps.push(lamp);
	}
}

/* Function: createRotor */
// This function creates the rotors that appear at the top of the window. A label is added to the
// rotor. Permutations, inverse permutations, and the offset are added / pushed to the rotor.
function createRotor() {
	for (let i = 0; i < ROTOR_LOCATIONS.length; i++) {
		let rotor = GCompound();
		let rotorRect = GRect(ROTOR_LOCATIONS[i].x - ROTOR_WIDTH / 2, ROTOR_LOCATIONS[i].y - ROTOR_HEIGHT / 2, ROTOR_WIDTH, ROTOR_HEIGHT);
		rotorRect.setFilled(true);
		rotorRect.setColor(ROTOR_BGCOLOR);
		rotor.add(rotorRect);
		
		let rotorLabel = new GLabel(ALPHABET[0], ROTOR_LOCATIONS[i].x, ROTOR_LOCATIONS[i].y);
		rotor.label = rotorLabel;
		rotorLabel.setFont(ROTOR_FONT);
      rotorLabel.setColor(ROTOR_COLOR);
      rotorLabel.setTextAlign("center");
      rotorLabel.setBaseline("middle");
      rotor.add(rotorLabel);

      let permutation = ROTOR_PERMUTATIONS[i];

      rotor.permutation = permutation;
      let inversePermutation = invertKey(permutation);
      rotor.inversePermutation = inversePermutation;
      let offset = 0;
      rotor.offset = offset;

      enigma.rotors.push(rotor);
      enigma.permutations.push(permutation);
      enigma.inversePermutations.push(inversePermutation);

      // Advances the rotor to the next letter when it is clicekd on
      rotor.clickAction = function(e) {
      	advanceRotor(rotor);
  
      };
      gw.add(rotor);
      
	}
}

// Responds to clicks if the object is not null
let clickAction = function(e) {
   	let object = gw.getElementAt(e.getX(), e.getY());
   	if (object !== null && object.clickAction !== undefined) {
   		object.clickAction(enigma);
   	}
   };

/* Function: advanceRotor */
// This function returns a boolean: false when no carry occurs, and true when the offset returns to
// 0. Takes the rotor object and advances it
function advanceRotor(rotor) {
	rotor.offset = (rotor.offset + 1) % ALPHABET.length;
	rotor.label.setLabel(ALPHABET[rotor.offset]);

	if (rotor.offset === 0) {
		return true;
	} else {
		return false;
	}
}

/* Function: applyPermutation */
// Calculates the index of the letter after shifting by the offset, searches for the character at the
// index of the permutation string, and then returns the index of the resulting character after
// subtracting the offset.
function applyPermutation(index, permutation, offset) {
	let newIndex = (index + offset) % permutation.length;
	let newLetter = permutation[newIndex];
	let resultIndex = (ALPHABET.indexOf(newLetter) - offset + ALPHABET.length) % ALPHABET.length;
	return resultIndex;
}

/* Function: invertKey */
// Takes a string / permutation and returns its inverse by searching through the letters in a cipher text
function invertKey(permutation) {
	let invertedKey = "";
	for (let i = 0; i < permutation.length; i++) {
		for (let j = 0; j < permutation.length; j++) {
			if (permutation[j] === ALPHABET[i]) {
				invertedKey += ALPHABET[j];
			}
		}
	}
	return invertedKey;
}
	createRotor();
	createLamp();
   gw.addEventListener("mousedown", mouseDownAction);
   gw.addEventListener("mouseup", mouseUpAction);
   gw.addEventListener("click", clickAction);

}