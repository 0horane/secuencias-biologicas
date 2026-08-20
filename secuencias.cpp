#include <iostream>
#include <vector>
#include <algorithm>


using namespace std;

int main(){
    string input;
    int k;
    cout << "Ingresar string \n";
    cin >> input;
    cout << "Ingrese un k";
    cin >> k;
    
    vector<string> res = {};

    for (int i = 0; i < input.size() - k + 1; i++) {
        res.push_back(input.substr(i,k));
    }

    sort(res.begin(), res.end());

    for (int i = 0; i < res.size(); i++) {
        cout << res[i] << '\n';
    } 


}