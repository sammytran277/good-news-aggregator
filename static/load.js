// This file contains the code for the load more button

$(document).ready(function() {

  // Get all the cards, which represent all the articles
  var anchors = document.querySelectorAll("div.card-columns > a");

  // Show the first 48 articles and hide the rest
  for (var i = 0, n = anchors.length; i < n; i++) {
    if (i <= 47) {
      anchors[i].classList.add("loaded");
    } else {
      anchors[i].setAttribute("style", "display: none;");
    }
  }

  // Detect when user clicks on the load more button
  $("#loadMore").click(function() {

    // Change button's inner HTML to a spinner
    $("#loadMore").html("<span class='spinner-border spinner-border-sm' role='status' aria-hidden='true'></span> Loading...");
    
    // Wait one second and change it back
    setTimeout(function() {
      $("#loadMore").html("Load More");
    }, 1000);

    // Wait one second so user can actually see the spinner
    setTimeout(function() {
      var filteredAnchors = document.querySelectorAll(".filtered");
      var counter = 0;
      
      /* Iterate through the filtered anchors and show the next 48 articles 
         if there are >= 48 articles left to show, otherwise just show the rest */
      filteredAnchors.forEach(anchor => {
        if (counter % 48 != 0 || counter == 0) {
          if(!anchor.classList.contains("loaded")) {
            anchor.removeAttribute("style");
            anchor.classList.add("loaded");
            counter++;
          }
        } else {
          anchor.setAttribute("style", "display: none;");
        }

        // Get a bool to determine whether or not to hide the load more buttom
        var removeButton = checkLoaded(filteredAnchors);

        if (removeButton) {
          $("#loadMore").attr("style", "display: none");
        }
      });
    }, 1000);
  });
});

function checkLoaded(filteredAnchors) {
  /* This function returns true if all filtered articles have been loaded, 
     otherwise it returns false */
  for (var i = 0, n = filteredAnchors.length; i < n; i++) {
    if (!filteredAnchors[i].classList.contains("loaded")) {
      return false;
    }
  }

  return true;
}