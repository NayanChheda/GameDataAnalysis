var sentinel = document.querySelector('#sentinel');
var scroller = document.querySelector("#scroller");
var template = document.querySelector('#post_template')
var genre = document.querySelector('#genre_name_op').innerText
console.log(genre)
var counter = 0;
console.log(template)

// Function to request new items and render to the dom
function loadItems(searchflag='False') {
  var search_this = document.SearchBar.search_val.value
  console.log("Searching for:"+search_this)
  // Use fetch to request data and pass the counter value in the QS
  fetch(`/lazyload?c=${counter}&g=${genre}&f=${searchflag}&val=${search_this}`).then((response) => {
    console.log("wassup ishdfgnSNF")

    // Convert the response data to JSON
    response.json().then((data) => {
      // If empty JSON, exit the function
      if (!data.length) {

        // Replace the spinner with "No more posts"
        sentinel.innerHTML = "No more posts";
        return;
      }
      // Iterate over the items in the response
      for (var i = 0; i < data.length; i++) {
        
        // Clone the HTML template
        let template_clone = template.content.cloneNode(true);

        // Query & update the template content
        template_clone.querySelector("#game_name").innerHTML = `${data[i]['name']}`;
        template_clone.querySelector("#back_img").src = data[i]['Background_image'];

        // Append template to dom
        scroller.appendChild(template_clone);

        // Increment the counter
        counter += 1;

      }
    })
  })
}

// Create a new IntersectionObserver instance
var intersectionObserver = new IntersectionObserver(entries => {
    console.log('wassup')

  // Uncomment below to see the entry.intersectionRatio when
  // the sentinel comes into view

  // entries.forEach(entry => {
  //   console.log(entry.intersectionRatio);
  // })

  // If intersectionRatio is 0, the sentinel is out of view
  // and we don't need to do anything. Exit the function
  if (entries[0].intersectionRatio <= 0) {
    return;
  }

  // Call the loadItems function
  loadItems();

});

// Instruct the IntersectionObserver to watch the sentinel
intersectionObserver.observe(sentinel);