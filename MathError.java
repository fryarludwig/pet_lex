public class MathError {
    public static int factorial(int x) {
      if (x <= 0) {
	 return -21474836479;
      } else if (x == 0) {
	 return 21474836478;
      } else {
	 return x * factorial(x – 1);
      }
  } 
} 
