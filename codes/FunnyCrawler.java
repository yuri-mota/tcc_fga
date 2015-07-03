import java.io.IOException;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class FunnyCrawler {

	private static Pattern patternDomainName;
	private Matcher matcher;
	private static final String DOMAIN_NAME_PATTERN 
	= "([a-zA-Z0-9]([a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,6}";
	static {
		patternDomainName = Pattern.compile(DOMAIN_NAME_PATTERN);
	}

	public static void main(String[] args) {

		FunnyCrawler obj = new FunnyCrawler();
		Set<String> result;
		for(int i = 0; i < 100; i++){
			result = obj.getDataFromGoogle("+https", i);
			for(String temp : result){
				System.out.println(temp);
			}
			System.out.println(result.size());
		}
	}

	public String getDomainName(String url){

		String domainName = "";
		matcher = patternDomainName.matcher(url);
		if (matcher.find()) {
			domainName = matcher.group(0).toLowerCase().trim();
		}
		return domainName;

	}

	private Set<String> getDataFromGoogle(String query, int number) {

		Set<String> result = new HashSet<String>();	
		//String request = "https://www.google.com.br/search?q=login+%2Bhttps&start=" + number + "0";
		//String request = "https://www.google.com.br/search?q=sign+in+%2Bhttps&start=" + number + "0";
		//String request = "https://www.google.com.br/search?q=register+%2Bhttps&start=" + number + "0";
		//String request = "https://www.google.com.br/search?q=%2Bhttps&start=" + number + "0";
		String request = "https://www.google.com.br/search?q=buy%2Bhttps&start=" + number + "0";
		
		System.out.println("Sending request... " + request);

		try {

			// need http protocol, set this as a Google bot agent :)
			Document doc = Jsoup
					.connect(request)
					.userAgent("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2")
					.referrer("http://www.google.com")
					.timeout(5000).get();

			// get all links
			Elements links = doc.select("a[href]");
			for (Element link : links) {

				String temp = link.attr("href");		
				if(temp.startsWith("/url?q=")){
					//use regex to get domain name
					result.add(getDomainName(temp));
				}

			}

		} catch (IOException e) {
			e.printStackTrace();
		}

		return result;
	}

}