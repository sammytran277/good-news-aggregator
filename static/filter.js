// This file contains the code for the entire filter feature

$(document).ready(function() {

  // Detect when user clicks on the filter button
  $("#filterButton").click(function() {

    // Prevent form submission so we can validate it ourselves
    $("#filter").submit(function(event) {
      event.preventDefault();
    });

    var websites = [];

    // Get all checked off websites and push value to websites array
    $.each($("input[name='websites']:checked"), function() {
      websites.push($(this).val());
    });

    // Check that user checked off at least one box
    if (!websites.length) {
      alert("Please select something!");
    } else {
      var anchors = document.querySelectorAll("div.card-columns > a");
      var filteredAnchors = [];
      var link;
      
      // Iterate through each anchor tag in anchors
      anchors.forEach(anchor => {
        link = anchor.getAttribute("href");

        /* Traditional loop here because forEach() doesn't have access to break
           Iterate through each website in websites and hide anchor if it is not
           one of the selected websites */
        for (var i = 0, n = websites.length; i < n; i++) {

          anchor.classList.remove("loaded");

          // Check if article link contains a filtered website
          if (!link.includes(websites[i])) {
            anchor.classList.remove("filtered", "loaded");
            anchor.setAttribute("style", "display: none;");
          } else {
            anchor.removeAttribute("style");
            anchor.classList.add("filtered");
            filteredAnchors.push(anchor);
            break;
          }
        }
      });

      var counter = 0;

      // Load the first 48 filtered articles and hide the rest
      filteredAnchors.forEach(anchor => {
        if (counter % 48 != 0 || counter == 0) {
          anchor.classList.add("loaded");
          counter++;
        } else {
          anchor.setAttribute("style", "display: none;");
        }
      });

      // Hide the button if there is no more content to show
      if (filteredAnchors.length < 48) {
        $("#loadMore").attr("style", "display: none");
      } else {
        $("#loadMore").removeAttr("style");
      }
    }
  });
});