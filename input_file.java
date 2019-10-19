class test{
    int d = 12;
    public static void main(String[] args) {
        int a = 10;
        int count = 0;
        while (a > count) {
            count = count + 1;
        }
        int b = 0;
        if (a > b) {
            b = a;
        } else {
            b = 10;
        }
        int c = 2;
        do {
            System.out.println("do while loop");
        } while(c++ < 5);
        hello(2);
    }
    static int hello(int d) {
        System.out.println("Hello, World!" + d);
        return 0;
    }
}