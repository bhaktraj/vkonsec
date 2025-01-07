var TIMEOUT = 3000;
var interval = setInterval(handleNext, TIMEOUT);
function handleNext() {

  var $radios = $('input[class*="slidel-radio"]');
  var $activeRadio = $('input[class*="slidel-radio"]:checked');

  var currentIndex = $activeRadio.index();
  var radiosLength = $radios.length;

  $radios
    .attr('checked', false);


  if (currentIndex >= radiosLength - 1) {

    $radios
      .first()
      .attr('checked', true);

  } else {

    $activeRadio
      .next('input[class*="slidel-radio"]')
      .attr('checked', true);

  }

}