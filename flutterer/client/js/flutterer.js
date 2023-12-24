/**
 * File: flutterer.js
 * ------------------
 * Contains the logic that makes Flutterer work, as well as all initialization.
 */
"use strict";

// Specify a list of valid users. (Extension opportunity: You can create an
// API route that lets users sign up, and then here, you can load a list of
// registered users.)
const USERS = [
    "Kaia Li",
    "Artur Carniero",
    "Colin Schultz",
    "Yubin Jee",
    "Ashlee Kupor",
    "Jerry Cain",
    "Avi Gupta",
    "Doris"
];

/**
 * Function: Flutterer
 * -------------------
 * Flutterer's entry point
 */
function Flutterer() {
    let allFlootsList = [];
    let selectedUser = USERS[0];
    let emptyPage = null;

    // Actions object containing functions that are defined below
    let actions = {
        changeSelectedUser: changeSelectedUser,
        createFloot: createFloot,
        deleteFloot: deleteFloot,
        openFlootInModal: openFlootInModal,
        closeModal: closeModal,
        createComment: createComment,
        deleteComment: deleteComment
    };

    postFloots();

    // Makes a request to load the floots
    function postFloots() {
        let req = AsyncRequest("/api/floots");
        req.setSuccessHandler(makeFlootsList);
        req.send();
    }


    // Updates the floots list
    function makeFlootsList(response) {
        let flootsList = JSON.parse(response.getPayload());
        allFlootsList = flootsList;
        renderPage(emptyPage);
    }

    // Draws / re-renders the page given the floot elements
    function renderPage(flootObject) {
        // Clears whatever is in the body
        while (document.body.lastChild != emptyPage) {
            document.body.removeChild(document.body.lastChild);
        }
        // Updates the MainComponent 
        document.body.appendChild(MainComponent(selectedUser, flootObject, allFlootsList, actions));
    }

    // Creates a new floot and makes an asynchronous request to post a new floot
    function createFloot(message) {
        let req = AsyncRequest("/api/floots");
        req.setMethod("POST");
        req.setPayload(JSON.stringify({
            username: selectedUser,
            message: message,
        }))
        req.setSuccessHandler(postFloots);
        req.send();
    }

    // Adds a new comment on a floot
    function createComment(flootID, comment) {
        let req = AsyncRequest("/api/floots/" + flootID + "/comments");
        req.setMethod("POST");
        req.setPayload(JSON.stringify({
            username: selectedUser,
            message: comment,
        }));
        req.setSuccessHandler(postFloots);
        req.send();
    }

    // Opens a floot in a modal
    // Renders the page with the selected floot
    function openFlootInModal(flootObject) {
        renderPage(flootObject);
    }

    // Updates the currentUser and then renders the page with
    // the updated user
    function changeSelectedUser(username) {
        selectedUser = username;
        renderPage(emptyPage);
    }

    // Deletes a floot by sending an asynchronous request
    function deleteFloot(flootID) {
        let req = AsyncRequest("/api/floots/" + flootID + "/delete");
        req.setMethod("POST");
        req.setPayload(JSON.stringify({
            username: selectedUser
        }))
        req.setSuccessHandler(postFloots);
        req.send();
    }

    // Closes the modal
    // Renders the page with no floot element
    function closeModal() {
        renderPage(emptyPage);
    }

    // Deletes a comment by sending an asynchronous request
    function deleteComment(flootID, commentID) {
        let req = AsyncRequest("api/floots/" + flootID + "/comments/" + commentID + "/delete");
        req.setMethod("POST");
        req.setPayload(JSON.stringify({
            username: selectedUser
        }));
        req.setSuccessHandler(postFloots);
        req.send();
    }
}

/**
 * Component: MainComponent
 * ------------------------
 * Constructs all the elements that make up the page.
 *
 * Parameters:
 *   * selectedUser: username of the logged-in user (string)
 *   * floots: an array of floot aggregates/objects that make up the news feed
 *   * actions: an aggregate containing a variety of functions that can be used
 *     to change the page or send data to the server (e.g. change the currently
 *     logged-in user, delete floots, etc.)
 *   * TODO: In Milestone 7: a parameter that contains the floot object that
 *     should be displayed in a modal, or null if no floot has been clicked and
 *     the modal should not be displayed
 *
 * Returns a node with the following structure:
 *   <div class="primary-container">
 *       <Sidebar />
 *       <NewsFeed />
 *   </div>
 */
function MainComponent(selectedUser, selectedFloot, floots, actions) {
    // Creates container element for main component
    let mainComponent = document.createElement("div");
    mainComponent.classList.add("primary-container");
    // Create sidebar with selected user options
    let sideBar = Sidebar(USERS, selectedUser, actions);
    // Creates news feed with posted floots
    let newsFeed = NewsFeed(selectedUser, floots, actions);
    // Append the sidebar and news feed to the container
    mainComponent.appendChild(sideBar);
    mainComponent.appendChild(newsFeed);
    // If a certain floot is selected, append it to the container in the modal
    if (selectedFloot != null) {
        mainComponent.appendChild(FlootModal(selectedFloot, selectedUser, actions));
    }
    return mainComponent;

}

/**
 * NOTE TO STUDENTS: you don't need to understand anything below.  It's fancy
 * JavaScript we need to help make the development process a little easier.
 *
 * The following code uses some Javascript magic so that all network requests
 * are logged to the browser console. You can still view all network requests
 * in the Network tab of the browser console, and that may be more helpful (it
 * provides much more useful information), but students may find this handy for
 * doing quick debugging.
 */
(() => {
    function log_info(msg, ...extraArgs) {
        console.info("%c" + msg, "color: #8621eb", ...extraArgs);
    }
    function log_success(msg, ...extraArgs) {
        console.info("%c" + msg, "color: #39b80b", ...extraArgs);
    }
    function log_error(msg, ...extraArgs) {
        console.warn("%c" + msg, "color: #c73518", ...extraArgs);
    }
    const _fetch = window.fetch;
    window.fetch = function(...args) {
        log_info(`Making async request to ${args[1].method} ${args[0]}...`);
        return new Promise((resolve, reject) => {
            _fetch(...args).then((result) => {
                const our_result = result.clone();
                our_result.text().then((out_text) => {
                    if (our_result.ok) {
                        log_success(`Server returned successful response for ${our_result.url}`);
                    } else {
                        log_error(`Server returned Error ${our_result.status} `
                            + `(${our_result.statusText}) for ${our_result.url}`,
                            out_text);
                    }
                    resolve(result);
                });
            }, (error) => {
                log_error('Error!', error);
                reject(error);
            });
        });
    };

    log_info("Did you know?", "For this assignment, we have added some code that "
        + "logs network requests in the JS console. However, the Network tab "
        + "has even more useful information. If you are having problems with API "
        + "calls, the Network tab may be a good place to check out; you can see "
        + "POST request bodies, full server responses, and anything else you might "
        + "desire there.");
})();

document.addEventListener("DOMContentLoaded", Flutterer);
