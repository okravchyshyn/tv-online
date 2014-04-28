

function embed_flash_player() {

   var embed = "<object id=\"player_id_1\" bgcolor=\"#000000\"" 
      + "type=\"application/x-shockwave-flash\" height=\"100%\" width=\"100%\">"
      + "<param value=\"true\" name=\"allowfullscreen\">"
      + "<param value=\"always\" name=\"allowscriptaccess\">"
      + "<param value=\"true\" name=\"seamlesstabbing\">"
      + "<param value=\"opaque\" name=\"wmode\">"
      + "</object>"

  var doc = document.getElementById("player_id");
  doc.innerHTML = embed; 

}

function f_1plus1() {
  embed_flash_player();
  //var url = "http://stream1115.tsn.ua:1935/streamlive/189931/playlist.m3u8";
  var url = "http://stream1115.tsn.ua:1935/streamlive/189931/playlist.m3u8"
  //var url = "http://content.bitsontherun.com/videos/i8oQD9zd-640.mp4";
  play(url);
};

function f_inter() {
 embed_flash_player();
 var uPlayer = new TnsVideoPlayer(
                {
                            id: "player_id_1",
                            autostart: true,
                            width: "100%",
                            height: "100%",

                            wmode: "opaque",
                            bgcolor: "#000000",
                            video: {
                                poster: "http://inter.ua/images/logo_420x337.jpg",
                                flash: {
                                    /* задание потока */
                                    stream: {
                                        url: "rtmpe://lb1.itcons.net.ua/inters-redir",
                                        media: [
					{
                                            url: "inter_3",
                                            bitrate: 1024,
                                            width: 720
                                        }, {
                                            url: "inter_2",
                                            bitrate: 512,
                                            width: 720
                                        }, {
                                            url: "inter_1",
                                            bitrate: 256,
                                            width: 720
                                        }     ]
                                           },

                                      },
                                    html5: {
                     stream: "http://lb1.itcons.net.ua:1935/inters/redirect.hls?smil:inter.smil"
                                    }
                                   },
                     }
               );
    uPlayer.play(1);
};


function play(url) {

    jwplayer("player_id_1").setup({
      'file': url,
'autostart':'true',
'allowfullscreen':'true',
'stretching':'fill',
height: "100%",
width: "100%",
    });
};


function f_ukraina() {
  embed_flash_player();
  var html = get_http_page("http://" + location.host +"/?channel=http://kanalukraina.tv/online/");
  var patt1=new RegExp("http://kanalukraina.tv/index.m3u8\\?token=[a-f0-9]*", "i");
  var url = patt1.exec(html);

  //var url = "http://kanalukraina.tv/index.m3u8?token=e60e7878aeedcff2730e53312f4121c04c004001";
  play(url[0]);
};


function tvx_provider(url) {

  var html = get_http_page("http://" + location.host + "/?channel=" + url );
  if( html != null ) {
    var em = search_element(html, "video-block");
    var embed = "<div id=\"video-block\"> " + em.innerHTML + " </div>";
    var doc = document.getElementById("player_id");
    doc.innerHTML = embed; 
   }
}


function f_2plus2() {
  tvx_provider("http://tvx.com.ua/tv/kanal-2-plus-2/");
};

function f_5kanal() {
  tvx_provider("http://tvx.com.ua/tv/5-kanal/");
}

function f_ictv() {
  tvx_provider("http://tvx.com.ua/tv/5-kanal/");
}

function f_tet() {
  tvx_provider("http://tvx.com.ua/tv/tet/");
}

function f_novyy_kanal() {
  tvx_provider("http://tvx.com.ua/tv/novy-kanal-online/");
}

function f_stb() {
  tvx_provider("http://tvx.com.ua/tv/kanal-stb/");
}

function f_pershyy() {
  tvx_provider("http://tvx.com.ua/tv/pervyj-nacionalnyj/");
}


function f_qtv() {
  tvx_provider("http://tvx.com.ua/tv/qtv-online/");
}

