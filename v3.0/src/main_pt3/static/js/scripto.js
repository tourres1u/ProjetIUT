var blipDim = '400px';

$('.blip-link').click(function(event){
  event.click();
  event.preventDefault();
  $('.blip-click', this).width(blipDim).height(blipDim);
  $('.link-content', this).addClass('clicked');
});

$('.blip-link').mouseleave(function(){
  if($('.link-content', this).hasClass('clicked')) {
    $('.blip-click', this).width(0).height(0);
    $('.link-content', this).removeClass('clicked');
  }
});