public class HelloWorld {
    public static void main(String[]  args) {
        System.out.println("Hello, World");
        var myWord7 = 12 ;
        var myWord7;
    }
}
public class HelloWorldError {
    public static void main(String[] largs1) {
        System.out.println("Hello, World");
    }
}

public class Math {
    public static int factorial(int x) {
      if (x <= 0) {
	 return -1;
      } else if (x == 0) {
	 return 1;
      } else {
	 return x * factorial(x – 1);
      }
  }
}
public class MathError {
    public static int factorial(int x, void y = 2) {
      if (x <= 0) {
	 return -21474836479;
      } else if (x == 0) {
	 return 21474836478;
      } else {
	 return x * factorial(x – 1);
      }
  }
}
public class NoError {
    public static int test1() {
	     int a = ;
		 a = b ** c;
  }
}
public class NoError {
    public static int test1() {   // test test test ! = ;
	    //  int a = ;
		//  a = b ** c;
  }
}
// }
