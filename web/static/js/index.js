/*
 * index.js
 * Copyright (C) 2015 Jakub Krajniak <jkrajniak@gmail.com>
 *
 * Distributed under terms of the GNU GPLv3 license.
 *
 * createImageLayer, imageOnload and imageOnclick by Richard Atterer
 *
   Copyright (C) 2007 Richard Atterer, richard©atterer.net
   This program is free software; you can redistribute it and/or modify it
   under the terms of the GNU General Public License, version 2. See the file
   COPYING for details. */

var imageNr = 0; // Serial number of current image
var finished = new Array(); // References to img objects which have finished downloading
var paused = false;
var socket = null;
var host = "http://localhost:8080/"

function createImageLayer() {
  var img = new Image();
  img.style.position = "absolute";
  img.style.zIndex = -1;
  img.onload = imageOnload;
  img.onclick = imageOnclick;
  img.src = host + "?action=snapshot&n=" + (++imageNr);
  var webcam = document.getElementById("webcam");
  webcam.insertBefore(img, webcam.firstChild);
}

// Two layers are always present (except at the very beginning), to avoid flicker
function imageOnload() {
  this.style.zIndex = imageNr; // Image finished, bring to front!
  while (1 < finished.length) {
    var del = finished.shift(); // Delete old image(s) from document
    del.parentNode.removeChild(del);
  }
  finished.push(this);
  if (!paused) createImageLayer();
}

function imageOnclick() { // Clicking on the image will pause the stream
  paused = !paused;
  if (!paused) createImageLayer();
}

function restartPage() {  
  paused = false;
  $("img#capture-preview").attr('src', '');
  $("#search").parent('div').removeClass('has-error has-success');
  $("#search").val("");
  $("#email").parent('div').removeClass('has-error has-success');
  $("#email").val("");

  $(".rank_cells").css('background-color', 'white');
  $("img#partial").attr('src', '');

  $("img#result").attr('src', '');
  $("#recipient").text("");

  createImageLayer();
  $.scrollTo("#step1", 800);
  $("#capture").prop('disabled', true)
  daemon_observer = setInterval(function() {
      socket.emit('ping daemon')
      }, 500)
}
