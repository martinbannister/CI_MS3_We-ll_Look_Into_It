document.addEventListener('DOMContentLoaded', function() {
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
    let FABs = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(FABs);
    let selectElems = document.querySelectorAll('select');
    if (selectElems) {
      M.FormSelect.init(selectElems);
    }
    let accords = document.querySelectorAll('.collapsible');
    M.Collapsible.init(accords);
    var tooltips = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltips);
  });

function checkRegisterForm(e) {
    let elems = e.target.elements;
    let pass1 = elems.password.value;
    let pass2 = elems.confirm_password.value;

    if (pass1 != pass2) {
      e.preventDefault();
      M.toast({html: 'Please ensure passwords match'});
      return false;
    } else {
      console.log('submitting form');
      return true;
    }
  }