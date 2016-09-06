package nz.govt.linz.AdminBoundaries;

/**
 * AdminBoundaries
 *
 * Copyright 2014 Crown copyright (c)
 * Land Information New Zealand and the New Zealand Government.
 * All rights reserved
 *
 * This program is released under the terms of the new BSD license. See the
 * LICENSE file for more information.
 */

import java.io.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class DABServletMain extends DABServlet {
	
	static final long serialVersionUID = 2;
	DABConnector dabc;
	
	public String docType = "<!doctype html public \"-//w3c//dtd html 4.0 transitional//en\">\n";
	
	public void init() throws ServletException {
		title = "DABm";
		message = "AIMS Extractor Main";
	}
	
	
	public void sendNotification(){
		//Send email to users informing them a new import is ready to review 
	}
	
	public void doGet(HttpServletRequest request, HttpServletResponse response)
		    throws IOException, ServletException {
		
		response.setContentType("text/html");
        PrintWriter out = response.getWriter();
        
        HttpSession session = request.getSession(true);
        Date created = new Date(session.getCreationTime());
        Date accessed = new Date(session.getLastAccessedTime());        
        
        Enumeration headerNames = request.getHeaderNames();
        while (headerNames.hasMoreElements()) {
			String headerName = (String) headerNames.nextElement();
			out.print("<br/>Header Name: <em>" + headerName);
			String headerValue = request.getHeader(headerName);
			out.print("</em>, Header Value: <em>" + headerValue);
			out.println("</em>");
		}
        
        out.println("<hr/>");
		String authHeader = request.getHeader("authorization");
		out.println("Auth Header: <em>" + authHeader);
		//String encodedValue = authHeader.split(" ")[1];
		//out.println("Base64-encoded Authorization Value: <em>" + encodedValue);
		//String decodedValue = Base64.base64Decode(encodedValue);
		//out.println("</em><br/>Base64-decoded Authorization Value: <em>" + decodedValue);
		out.println("</em><hr/>");
        
        out.println(docType +
                "<html><head>\n" +
                getHead() +
                "</head>\n<body><div id=\"container\">" +
                getBodyHeader() +
                getBodyTitle() +
                getAuthForm() +
                "</div></body></html>");
        out.println("Created: " + created + "</br>");
        out.println("Last Accessed: " + accessed + "</br>");
	}
	
	protected String getAuthForm(){
		return String.join("\n"
				,"<form action=\"sum\" method=\"GET\"><table>"
				,"<tr><td>AIMS username:</td><td><input type=\"text\" name=\"user\"></td></tr>"
				,"<tr><td>AIMS password:</td><td><input type=\"text\" name=\"pass\"/></td></tr>"
				,"<tr><td span=\"2\"><input type=\"submit\" value=\"Login\"/></td></tr>"
				,"</table></form>");
	}
}
