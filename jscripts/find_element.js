function get_http_page(url) {
  
  var xhttp = null;
   
  if (window.XMLHttpRequest)  {
    xhttp=new XMLHttpRequest();
  } else {
    xhttp=new ActiveXObject("Microsoft.XMLHTTP");
  } 

   //xhttp.setRequestHeader("Access-Control-Allow-Origin","*");
  xhttp.open("GET",url,false);
  xhttp.send(null);
  if(xhttp.status == 200) {
      return xhttp.responseText;
  } else {
      return null;
  }

}

function search_element(html_page, elem_name) {
   var xmlDoc=loadXMLString(html_page);
   var doms = xmlDoc.getElementsByTagName("div");
   var elem = findElementByName(xmlDoc.childNodes, elem_name);
   changePlayerSize(elem);
   return elem;
}


function findElementByName(domObj, elemName) {
   for(var i = 0; i < domObj.length; i++) {
        var dom = domObj[i];
        var t =  typeof(dom);  
        var attr = 0;
        if ("id" in dom) { attr = 1;}
        //var a = dom.attr("id")
        if (attr && dom.id == elemName) {
            return dom;
        }
        dom = findElementByName(dom.childNodes, elemName);
        if (dom != null) return dom;
   }
   return null;
}

function changePlayerSize(video_block) {

  //parser=new DOMParser();
  //xmlDoc=parser.parseFromString(embedTxt,"text/html");
  var elems = video_block.getElementsByTagName("embed");
  if (elems.length > 0) {
  
     var em = elems[0];
     //var w = em.getAttribute("width");
     em.setAttribute("width","100%");
     em.setAttribute("hieght","100%");
     var m = em.outerHTML ;
     //document.write("DOM Object " + m + " <br>");
  }


}

function loadXMLString(txt)
{
if (window.DOMParser)
  {
  parser=new DOMParser();
  xmlDoc=parser.parseFromString(txt,"text/html");
  }
else // code for IE
  {
  xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
  xmlDoc.async=false;
  xmlDoc.loadXML(txt);
  }
return xmlDoc;
}

