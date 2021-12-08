document.addEventListener('DOMContentLoaded', function() {
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
    let FABs = document.querySelectorAll('.fixed-action-btn');
    M.FloatingActionButton.init(FABs);
    let selectElems = document.querySelectorAll('select');
    if (selectElems) {
      M.FormSelect.init(selectElems);
    }
  });

function checkRegisterForm(e) {
    e.preventDefault();
    let elems = e.target.elements;
    let pass1 = elems.password.value;
    let pass2 = elems.confirm_password.value;

    if (pass1 != pass2) {
      alert('Please ensure passwords match');
      return false;
    } else {
      return true;
    }
  }