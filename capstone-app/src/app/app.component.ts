import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  datePipe: DatePipe = new DatePipe('en-US');
  displayDate: any;
  displayTime: any;
  alarmTime: any;
  subscription!: Subscription;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    setInterval(() => {
      this.displayDate = this.getFormattedDate();
      this.displayTime = this.getFormattedTime();
    }, 1000);

    setInterval(() => {
      this.subscription = this.http.get('assets/alarm_time.txt', { responseType: 'text' }).subscribe((data: any) => {
        this.alarmTime = data;
      })
      this.subscription.unsubscribe;
    }, 250);
  }

  getFormattedDate() {
    var date = new Date();
    var transformDate = this.datePipe.transform(date, 'MM-dd-yyyy');
    return transformDate;
  }

  getFormattedTime() {
    var date = new Date();
    var transformDate = this.datePipe.transform(date, 'hh:mm:ss a');
    return transformDate;
  }
}

