/*
 * File: Wordle.js
 * -----------------
 * This program implements the Wordle game.
 */
"use strict";
/**
 * GAME RULES CONSTANTS
 * ---------------------
 */
const NUM_LETTERS = 5;  // The number of letters in each guess 
const NUM_GUESSES = 6;  // The number of guesses the player has to win

/**
 * SIZING AND POSITIONING CONSTANTS
 * --------------------------------
 */
const SECTION_SEP = 32; // The space between the grid, alert, and keyboard sections
const GUESS_MARGIN = 8; // The space around each guess square
const GWINDOW_WIDTH = 400;  // The width of the GWindow

// The size of each guess square (computed to fill the entire GWINDOW_WIDTH)
const GUESS_SQUARE_SIZE =
                        (GWINDOW_WIDTH - GUESS_MARGIN * 2 * NUM_LETTERS) / NUM_LETTERS;

// Height of the guess section in total
const GUESS_SECTION_HEIGHT =
                           GUESS_SQUARE_SIZE * NUM_GUESSES + GUESS_MARGIN * NUM_GUESSES * 2;

// X and Y position where alerts should be centered
const ALERT_X = GWINDOW_WIDTH / 2;
const ALERT_Y = GUESS_SECTION_HEIGHT + SECTION_SEP;

// X and Y position to place the keyboard
const KEYBOARD_X = 0;
const KEYBOARD_Y = ALERT_Y + SECTION_SEP;

// GWINDOW_HEIGHT calculated to fit everything perfectly.
const GWINDOW_HEIGHT = KEYBOARD_Y + GKeyboard.getHeight(GWINDOW_WIDTH);


/**
 * STYLISTIC CONSTANTS
 * -------------------
 */
const COLORBLIND_MODE = false; // If true, uses R/G colorblind friendly colors

// Background/Border Colors
const BORDER_COLOR = "#3A3A3C"; // Color for border around guess squares
const BACKGROUND_DEFAULT_COLOR = "#121213";
const KEYBOARD_DEFAULT_COLOR = "#818384";
const BACKGROUND_CORRECT_COLOR = COLORBLIND_MODE ? "#E37E43" : "#618C55"; 
const BACKGROUND_FOUND_COLOR = COLORBLIND_MODE ? "#94C1F6" : "#B1A04C";
const BACKGROUND_WRONG_COLOR = "#3A3A3C";

// Text Colors
const TEXT_DEFAULT_COLOR = "#FFFFFF";
const TEXT_ALERT_COLOR = "#B05050";
const TEXT_WIN_COLOR = COLORBLIND_MODE ? "#94C1F6" : "#618C55";
const TEXT_LOSS_COLOR = "#B05050";

// Fonts
const GUESS_FONT = "700 36px HelveticaNeue";
const ALERT_FONT = "700 20px HelveticaNeue";


/**
 * Accepts a KeyboardEvent and returns
 * the letter that was pressed, or null
 * if a letter wasn't pressed.
 */
function getKeystrokeLetter(e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return null;
    const key = e.key.toLowerCase();

    if (!/^[a-z]$/.exec(key)) return null;

    return key;
}

/**
 * Accepts a KeyboardEvent and returns true
 * if that KeyboardEvent was the user pressing
 * enter (or return), and false otherwise.
 */
function isEnterKeystroke(e) {
    return (
                !e.altKey &&
                !e.ctrlKey &&
                !e.metaKey &&
                (e.code === "Enter" || e.code === "Return")
                );
}

/**
 * Accepts a KeyboardEvent and returns true
 * if that KeyboardEvent was the user pressing
 * backspace (or delete), and false otherwise.
 */
function isBackspaceKeystroke(e) {
    return (
                !e.altKey &&
                !e.ctrlKey &&
                !e.metaKey &&
                (e.code === "Backspace" || e.code === "Delete")
                );
}

/**
 * Accepts a string, and returns if it is a valid English word.
 */
function isEnglishWord(str) {
    return _DICTIONARY.has(str) || _COMMON_WORDS.has(str);
}

/**
 * Returns a random common word from the English lexicon,
 * that is NUM_LETTERS long.
 *
 * Throws an error if no such word exists.
 */
function getRandomWord() {
    const nLetterWords = [..._COMMON_WORDS].filter(
                           (word) => word.length === NUM_LETTERS
                           );

    if (nLetterWords.length === 0) {
        throw new Error(
                    `The list of common words does not have any words that are ${NUM_LETTERS} long!`
                    );
    }

    return nLetterWords[randomInteger(0, nLetterWords.length)];
}

/** Main Function: Wordle */
// This function calls the Wordle game. A user guesses a word that is stored by the computer and has five chances
// to guess a word. ith each guess that is entered, the user receives more information about the secret word.
function Wordle() {
  const gw = new GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT);
  let x0 = GUESS_MARGIN;
  let y0 = GUESS_MARGIN;
  // Define state variables
  let secretWord = getRandomWord().toUpperCase();
  let wordGuess = ["", "", "", "", "", ""];
  let numGuesses = 0;
  let currentGuess = "";
  let isCompleteGuess = false;
  let gameOver = false;
  let alertMessage = null;
  let square = null;
  let keyboard = new GKeyboard(KEYBOARD_X, KEYBOARD_Y, GWINDOW_WIDTH,
                               TEXT_DEFAULT_COLOR, KEYBOARD_DEFAULT_COLOR);
  gw.add(keyboard);

  /* Function: createGuessSquare */
  // This function creates the square and places the letter inside each square.
  function createGuessSquare(letter, color, x0, y0) {
      // Create individual square
      square = new GRect(x0, y0, GUESS_SQUARE_SIZE, GUESS_SQUARE_SIZE);
      square.setFilled(true);
      square.setColor(BORDER_COLOR);
      square.setFillColor(color);
      gw.add(square);
      // Create the letter that is inside the square
      let label = new GLabel(letter);
      label.setFont(GUESS_FONT);
      label.setColor(TEXT_DEFAULT_COLOR);
      label.setLocation(x0 + GUESS_SQUARE_SIZE / 2, y0 + GUESS_SQUARE_SIZE / 2);
      label.setTextAlign("center");
      label.setBaseline("middle");
      gw.add(label);
  }
  /* Function: createGuessRow */
  // Accepts the array of word guesses, creates the rows that fill the grid, updates the x position of
  // each square, and then updates the color of the square.
  function createGuessRow(wordGuess, y0) {
    let greenLetters = [];
    let yellowLetters = [];
    let frequencies = {};

    for (let i = 0; i < secretWord.length; i++) {
        frequencies[secretWord.charAt(i)] = 0;
    }
     for (let i = 0; i < secretWord.length; i++) {
        frequencies[secretWord.charAt(i)]++;
    }
    // If the guess letter and the secret letter are the same and in the same position, then add the index of
    // the green letter placement to an array called greenLetters and decrement the frequencies list in
    // the places of the guess letter
    for (let i = 0; i < wordGuess.length; i++) {
      let guessLetter = currentGuess.charAt(i).toUpperCase();
      let secretLetter = secretWord.charAt(i).toUpperCase();
      if (guessLetter === secretLetter) {
        greenLetters.push(i);
        frequencies[guessLetter]--;
      }
    }

    // If the secret word includes the guess letter (potential yellow) and the frequencies value is greater than
    // 0, then push those indices to the array yellowLetters and decrement the frequences list in the places of
    // the guess letter.
    for (let i = 0; i < wordGuess.length; i++) {
      let guessLetter = currentGuess.charAt(i).toUpperCase();
      let secretLetter = secretWord.charAt(i).toUpperCase();
      if (secretWord.includes(guessLetter) && frequencies[guessLetter] > 0) {
          yellowLetters.push(i);
          frequencies[guessLetter]--;        
      }
    }

    // Updates the colors based on the greenLetters and yellowLetters arrays. The color is the correct color. 
    // Redraws the grid and updates the keyboard color
    let x0 = GUESS_MARGIN;
    for (let i = 0; i < wordGuess.length; i++) {
      let color = BACKGROUND_WRONG_COLOR;
      if (greenLetters.includes(i) && isCompleteGuess) color = BACKGROUND_CORRECT_COLOR;
      else if (yellowLetters.includes(i) && isCompleteGuess) color = BACKGROUND_FOUND_COLOR; 
      let guessLetter = currentGuess.charAt(i).toUpperCase();
      createGuessSquare(guessLetter, color, x0, y0);
      x0 += GUESS_SQUARE_SIZE + GUESS_MARGIN * 2;
      updateKeyboardColor(guessLetter, color);
    }

  }

  /* Function: createGuessGrid */
  // Creates the grid by drawing the rows depending on how many guesses that the user has inputted.
  // The y value of the rows is also updated here and is increased with each guess that is submitted.
  function createGuessGrid(wordGuess) {
      y0 = (GUESS_SQUARE_SIZE + GUESS_MARGIN * 2) * numGuesses;
      for (let i = 0; i < wordGuess.length; i++) {
          createGuessRow(wordGuess[i].toUpperCase(), y0 + GUESS_MARGIN);
      }
  }

  /* Function: createAlert */
  // Accepts a message and the color of the text and adds an alert message to the user's screen.
  function createAlert(message, color) {
      alertMessage = new GLabel(message);
      alertMessage.setFont(ALERT_FONT);
      alertMessage.setColor(color);
      alertMessage.setLocation(ALERT_X, ALERT_Y);
      alertMessage.setTextAlign("center");
      alertMessage.setBaseline("middle");
      gw.add(alertMessage);
  }

  /* Function: updateKeyboardColor */
  // Changes the color of the on-screen keyboard's keys.
  function updateKeyboardColor(letter, color) {
      if (keyboard !== null && keyboard.getKeyColor(letter) !== BACKGROUND_CORRECT_COLOR) {
          if (keyboard.getKeyColor(letter) === BACKGROUND_FOUND_COLOR
                  || keyboard.getKeyColor(letter) === BACKGROUND_WRONG_COLOR) {
              return;
          }
          keyboard.setKeyColor(letter, color);
      }
  }

  /* Function: buildWord */
  // Accepts a letter and adds the letter to the user's current guess to build a word.
  // The current guess then becomes an entry of the array "wordGuess" which holds the user's
  // list of guesses.
  function buildWord(letter) {
      if (alertMessage !== null) {
          gw.remove(alertMessage);
      }
      if (gameOver) {
          return;
      }
      if (currentGuess.length < NUM_LETTERS) {
          currentGuess += letter;
      }
      wordGuess[numGuesses] = currentGuess;
      createGuessRow(currentGuess, GUESS_MARGIN + numGuesses * (GUESS_SQUARE_SIZE + GUESS_MARGIN * 2));
  }

  /* Function: deleteLetter */
  // Deletes a letter if the current guess has more than one letter inputted. Creates a grid
  // of the string after a letter is deleted.
  function deleteLetter(word) {
      if (currentGuess.length > 0) {
          currentGuess = currentGuess.substring(0, currentGuess.length - 1);
          draw();
      } else if (currentGuess.length === 1) {
          currentGuess = "";
      }
      wordGuess[numGuesses] = currentGuess;
      createGuessGrid(wordGuess);

  }

  /* Function: enterWord */
  // Allows a word to be entered as a guess and displayed on the screen if it is an English word
  // and if it has the right number of letters (five letters). Once a word is entered, the number of
  // guesses is incremented by one. If the user guesses the secret word or if the user's guesses surpass
  // the number of allowable attempts, an alert is displayed. An alert is also displayed if the word that is
  // entered is not an empty string or not an English word.
  function enterWord() {
      if (isEnglishWord(currentGuess) && currentGuess.length === NUM_LETTERS) {
          isCompleteGuess = true;
          createGuessGrid(wordGuess);
          numGuesses++;

          if (currentGuess.toUpperCase() === secretWord) {
              createAlert("You won!", TEXT_WIN_COLOR);
              gameOver = true;
          } else if (numGuesses >= NUM_GUESSES) {
              createAlert("You lost!", TEXT_LOSS_COLOR);
              gameOver = true;
          }
          currentGuess = "";
          isCompleteGuess = false;
      }
      else {
          if (currentGuess !== "") {
              createAlert(currentGuess.toUpperCase() + " is not a word!", TEXT_ALERT_COLOR);
          }
      }

  }

  /* Function: useKeyboard */
  // Connects the computer keyboard to the on-screen keyboard with buttons such as enter, backspace,
  // and the letter keys.
  function useKeyboard(e) {
      if (isEnterKeystroke(e)) {
          enterWord(e);
      } else if (isBackspaceKeystroke(e)) {
          deleteLetter(e);
      } else {
          let keyInput = getKeystrokeLetter(e);
          buildWord(keyInput);
      }
  }

  /* Function: draw */
  // Draws the guess grid, the alerts, and the keyboard.
  function draw() {
      createGuessGrid(currentGuess);

      if (alertMessage) {
          gw.add(alertMessage);
      }
      gw.add(keyboard);
  }
  draw();

  // Responds to keyboard clicks, enter button, backspace button, and links the computer keyboard to the on-screen keyboard
  keyboard.addEventListener("keyclick", buildWord);
  keyboard.addEventListener("enter", enterWord);
  keyboard.addEventListener("backspace", deleteLetter);
  gw.addEventListener("keydown", useKeyboard);
}
