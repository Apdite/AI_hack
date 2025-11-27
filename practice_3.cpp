#include <iostream>
#include <cstdlib>
#include <cmath>
#include <fstream>
#include <string>
#include <algorithm>


using namespace std;
//1+
int task31()
{
    string filename = "31.txt";
    string lin;
    
    ofstream outfile(filename);
    
    if (!outfile.is_open()) {
        cout << "Ошибка создания файла!" << endl;
        return 404;
    }
    
    cout << "Файл создан успешно." << endl;
    cout << "Введите текст для записи в файл (для завершения введите пустую строку):" << endl;

    while (true) {
        getline(cin, lin);
        if (lin.empty()) {
            break;
        }
        outfile << lin << endl;
    }
    
    outfile.close();
    cout << "Данные успешно записаны в файл." << endl << endl;
    
    ifstream infile(filename);
    
    if (!infile.is_open()) {
        cout << "Ошибка открытия файла для чтения!" << endl;
        return 1;
    }
    
    cout << "Содержимое файла :" << endl;
    
    while (getline(infile, lin)) {
        cout << lin << endl;
    }
    
    infile.close();
    
    cout << "Файл закрыт" << endl;
    return 0;
}

//2+
int task32()
{
    string fileloc, line;
    fileloc = "/Users/bogdan/Desktop/practice_c++/practice_1_sem/123.txt";
    ifstream firstfile(fileloc);
    
    if (firstfile.is_open())
    {
        cout << "Файл открыт" << endl;
        while (getline(firstfile, line))
        {
            string cur = "";
            string buf = "";  // накопитель чисел
            
            for (char sym : line)
            {
                if (isdigit(sym))
                {
                    cur += sym;
                }
                else
                {
                    if (!cur.empty())
                    {
                        if (!buf.empty())
                            buf += " ";
                        buf += cur;
                        cur = "";
                    }
                }
            }
            if (!cur.empty())
            {
                if (!buf.empty())
                    buf += " ";
                buf += cur;
            }

            if (!buf.empty())
                cout << buf << endl;
        }
    }
    else {
        cout << "Ошибка открытия файла" << endl;
    }
    
    firstfile.close();
    return 0;
}

//3 +
int task33()
{
    setlocale(LC_ALL, "RUS");
    string s;
    cout << "Введите строку содержащую буквы русского или латинского алфавита " << endl;
    getline(cin, s);
    
    double n = s.length();
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-i-1; j++) {

            if (tolower(s[j]) > tolower(s[j+1])) {
                swap(s[j], s[j+1]);
            }
        }
    }
    
    cout << s << endl;
    return 0;
}

//4 +
int task34()
{
    int a, b, m, n, f = 0;
    cout << "Введите значение a (m = a)" << endl;
    if (!(cin>>a))
    {
        cout << "Введен не верный тип данных" << endl;
        return  0;
    }
    cout << "Введите значение b (n = b)" << endl;
    if (!(cin>>b))
    {
        cout << "Введен не верный тип данных" << endl;
        return  0;
    }
    if (a<0 && b<0){
        f = 2;
    }
    if(a ==0 || b==0){
        cout<<"Не корректно"<<endl;
        return 0;
    }
    a = abs(a);
    b = abs(b);
    m = abs(a);
    n = abs(b);
    while ((a!=0) and (b!=0))
    {
        if (a>b)
        {
            a = a % b;
        }
        else{
            b = b % a;
        }
    }
    if (f == 2){
        cout << "Наибольший общий делитель (найденный делением): " << (a + b)*(-1)  << endl;
    }
    else{
        cout << "Наибольший общий делитель (найденный делением): " << (a + b)  << endl;
    }
    if (a==0 or b==0){
        if (a!=0){
            cout << "Наибольший общий делитель (найденный вычитанием): " << a << endl;
            return 0;
        }
        else{
            cout << "Наибольший общий делитель (найденный вычитанием): " << b << endl;
            return 0;
        }
    }
    while (m!=n)
    {
        if (m > n){
            m = m - n;
        }
        else{
            n = n - m;
        }
    }
    if (f == 2){
        cout << "Наибольший общий делитель (найденный вычитанием): " << m * (-1)  << endl;
    }
    else{
        cout << "Наибольший общий делитель (найденный вычитанием): " << m  << endl;
    }
    return 0;
}
//5 +
int task35()
{
    double N ;
    cout << "Введите значение больше 2-х: " << endl;
    if (!(cin >> N) || N < 2 || (N != floor(N)))
    {
        cout << "Введен не верный тип данных" << endl;
        return 0;
    }
    
    // массив чисел от 0 до N
    int* primes = new int[N + 1];
    for (int i = 0; i <= N; i++) {
        primes[i] = i;
    }
    primes[1] = 0;
    int i = 2;
    while (i < N)
    {
        if (primes[i] != 0)
        {
            int j = i * 2;
            while (j <= N)
            {
                primes[j] = 0;
                j = j + i;
            }
        }
        i += 1;
    }
    // Вывод 
    cout << "простые числа до " << N << ":" << endl;
    bool flag = true;
    for (int k = 2; k <= N; k++)
    {
        if (primes[k] != 0)
        {
            if (!flag) {
                cout << " ";
            }
            cout << primes[k];
            flag = false;
        }
    }
    cout << endl;
    
    delete[] primes; //освобождение памяти
    return 0;
}
//6 +
int task36(){
    int i = 0;
    double sum = 0.0, num;

      
      ofstream file("36.txt");
      while (i != 10) {
          i += 1;
          cout << i << ") ";
          if (cin >> num) {
              file << num << "\n";
          }
        else {
            cout << "Incorrect" << endl;
            return 0;
        }
      }
      file.close();
      
      ifstream ifile("36.txt");
      while (i != 20) {
          ifile >> num;
        sum += num;
        i ++;
      }
      ifile.close();
      
      cout << "Сумма = " << sum << endl;
      return 0;
    
}

int main3()
{
    task32();
    return 0;
}
