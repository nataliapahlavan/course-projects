/**
 * File: match-the-flag-constants.js
 * ---------------------------------
 * Defines a collection of constants needed to fully realize the
 * Match The Flag application.
 */
"use strict";

/*
 * Country names whose flags appear in the application.  The names of the
 * PNG image files are the same as the country names, except that
 * they live in an images folder, and their file names are all lowercase.
 * All named images are 72px square.
 */
const COUNTRIES = [
   "Belize", "Brazil", "China", "Colombia", 
   "Egypt", "Finland", "Greece", "India"
];
const NUM_COUNTRIES = COUNTRIES.length;

/*
 * The amount of time, in milliseconds, to delay after a
 * second flag is exposed.  What happens after the delay
 * depends on whether the two exposed flags match.  The delay,
 * however, is the same regardless.
 */
const DELAY = 1000; // im milliseconds

/*
 * Two additional names of 72px square images.  The first
 * is the one drawn on behalf of concealed flags that have
 * yet to be matched.  The second is drawn on behalf of
 * flags that have already been matched.
 */
const COVER_IMAGE = "images/cover.png";
const MATCHED_IMAGE = "images/transparent.png";

