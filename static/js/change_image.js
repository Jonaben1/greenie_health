// Select the container element
var container = document.querySelector(".row");

// Define a function that fetches the list of posts and updates the elements
function changePosts() {
  // Make a fetch request to the Django view that returns the list of posts as JSON
  fetch("/blog-list/")
    .then(response => response.json())
    .then(data => {
      // Clear the container element
      container.innerHTML = "";
      // Loop through each post in the data
      for (var post of data) {
        // Create new HTML elements for each post
        var col = document.createElement("div");
        col.className = "col-md-4";
        var card = document.createElement("div");
        card.className = "card mb-4";
        var img = document.createElement("img");
        img.className = "card-img-top img-fluid";
        img.setAttribute("src", post.image_url);
        img.setAttribute("alt", post.title);
        var body = document.createElement("div");
        body.className = "card-body";
        var title = document.createElement("h5");
        title.className = "card-title";
        title.textContent = post.title;
        var link = document.createElement("a");
        link.className = "btn btn-primary";
        link.setAttribute("href", post.detail_url);
        link.textContent = "Read more";
        // Append the elements to the container element
        body.appendChild(title);
        body.appendChild(link);
        card.appendChild(img);
        card.appendChild(body);
        col.appendChild(card);
        container.appendChild(col);
      }
    })
    .catch(error => console.error(error));
}

// Call the function every 5 seconds using setInterval
setInterval(changePosts, 5000);

